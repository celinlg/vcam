import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from utils import run_command, ADB
from config import COLOR_SUCCESS, COLOR_DANGER

class ManageTab:
    def __init__(self, parent, app_cache):
        self.tab = parent
        self.app_cache = app_cache
        self.setup_manage_tab()

    def setup_manage_tab(self):
        header = ctk.CTkFrame(self.tab)
        header.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(header, text="📥 Instalar APK do PC", fg_color=COLOR_SUCCESS, command=self.install_apk).pack(side="left", padx=10)
        
        self.manage_search = ctk.CTkEntry(self.tab, placeholder_text="🔎 Buscar app para desinstalar...")
        self.manage_search.pack(fill="x", padx=15, pady=5)
        self.manage_search.bind("<KeyRelease>", self.filter_manage)
        
        self.manage_scroll = ctk.CTkScrollableFrame(self.tab)
        self.manage_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    def install_apk(self):
        file = filedialog.askopenfilename(filetypes=[("APK Files", "*.apk")])
        if file:
            threading.Thread(target=lambda: messagebox.showinfo("Instalação", f"Resultado: {run_command([ADB, 'install', '-r', file])[:100]}")).start()

    def filter_manage(self, e):
        q = self.manage_search.get().lower()
        self.render_manage_list([p for p in self.app_cache if q in p.lower()])

    def render_manage_list(self, lista):
        for w in self.manage_scroll.winfo_children():
            w.destroy()
        for p in lista[:100]:
            f = ctk.CTkFrame(self.manage_scroll)
            f.pack(fill="x", pady=1)
            ctk.CTkLabel(f, text=p, anchor="w").pack(side="left", padx=10, expand=True, fill="x")
            ctk.CTkButton(f, text="Desinstalar", width=100, fg_color=COLOR_DANGER,
                         command=lambda pkg=p: self.uninstall_app(pkg)).pack(side="right", padx=5)

    def uninstall_app(self, pkg):
        if messagebox.askyesno("Confirmar", f"Deseja desinstalar {pkg}?"):
            threading.Thread(target=lambda: run_command([ADB, "uninstall", "--user", "0", pkg])).start()

    def update_list(self):
        self.render_manage_list(self.app_cache)
