import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from utils import run_command, ADB
from config import COLOR_SUCCESS, COLOR_DANGER

class ManageTab:
    def __init__(self, parent, app_cache, user_selector, load_apps_callback):
        self.tab = parent
        self.app_cache = app_cache
        self.user_selector = user_selector
        self.load_apps_callback = load_apps_callback
        self.status_label = None
        self.setup_manage_tab()

    def set_status_callback(self, status_label):
        self.status_label = status_label

    def setup_manage_tab(self):
        header = ctk.CTkFrame(self.tab)
        header.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(header, text="📥 Instalar APK", fg_color=COLOR_SUCCESS,
                     command=self.install_apk).pack(side="left", padx=10)
        
        self.manage_search = ctk.CTkEntry(header, placeholder_text="🔎 Buscar app para desinstalar...", width=350)
        self.manage_search.pack(side="left", padx=10, fill="x", expand=True)
        self.manage_search.bind("<KeyRelease>", lambda e: self.render_manage_list())
        
        ctk.CTkButton(header, text="🔄 Atualizar Lista",
                     command=self.load_apps_callback).pack(side="right", padx=10)

        self.manage_scroll = ctk.CTkScrollableFrame(self.tab)
        self.manage_scroll.pack(fill="both", expand=True, padx=10, pady=5)

    def render_manage_list(self):
        for w in self.manage_scroll.winfo_children():
            w.destroy()
        
        query = self.manage_search.get().lower()
        
        for p in self.app_cache:
            if query in p.lower():
                f = ctk.CTkFrame(self.manage_scroll)
                f.pack(fill="x", pady=2)
                
                ctk.CTkLabel(f, text=f"📦 {p}", anchor="w").pack(side="left", padx=10, expand=True, fill="x")
                
                ctk.CTkButton(f, text="Desinstalar", width=100, fg_color=COLOR_DANGER,
                             command=lambda pkg=p: self.uninstall_app(pkg)).pack(side="right", padx=5)

    def uninstall_app(self, pkg):
        user_id = self.user_selector.get()
        if messagebox.askyesno("Confirmar", f"Deseja desinstalar {pkg} para o usuário {user_id}?"):
            if self.status_label:
                self.status_label.configure(text=f"Desinstalando {pkg}...", text_color="orange")
            def task():
                res = run_command([ADB, "shell", "pm", "uninstall", "--user", user_id, pkg])
                self.tab.after(0, lambda: [
                    messagebox.showinfo("Resultado", res),
                    self.load_apps_callback(),
                    self.status_label.configure(text="Desinstalação concluída", text_color="green") if self.status_label else None
                ])
            threading.Thread(target=task, daemon=True).start()

    def install_apk(self):
        f = filedialog.askopenfilename()
        if f:
            threading.Thread(target=lambda: messagebox.showinfo("Info", run_command([ADB, "install", "-r", "--user", self.user_selector.get(), f]))).start()
