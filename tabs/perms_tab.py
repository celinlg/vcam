import customtkinter as ctk
import threading
import re
from utils import run_command, ADB
from config import COLOR_SUCCESS, COLOR_DANGER

class PermsTab:
    def __init__(self, parent, app_cache):
        self.tab = parent
        self.app_cache = app_cache
        self.setup_perms_tab()

    def setup_perms_tab(self):
        self.perm_search = ctk.CTkEntry(self.tab, placeholder_text="🔎 Buscar app para permissões...")
        self.perm_search.pack(fill="x", padx=15, pady=15)
        self.perm_search.bind("<KeyRelease>", self.filter_perms)
        
        self.perm_scroll = ctk.CTkScrollableFrame(self.tab)
        self.perm_scroll.pack(fill="both", expand=True)

    def filter_perms(self, e):
        q = self.perm_search.get().lower()
        self.render_perms_list([p for p in self.app_cache if q in p.lower()])

    def render_perms_list(self, lista):
        for w in self.perm_scroll.winfo_children():
            w.destroy()
        for p in lista[:100]:
            ctk.CTkButton(self.perm_scroll, text=f"🔐 {p}", anchor="w", fg_color="transparent", border_width=1,
                         command=lambda pkg=p: self.open_permission_panel(pkg)).pack(fill="x", pady=1)

    def open_permission_panel(self, pkg):
        pop = ctk.CTkToplevel(self.tab)
        pop.title(f"Permissões: {pkg}")
        pop.geometry("800x700")
        pop.attributes("-topmost", True)
        
        f_search = ctk.CTkEntry(pop, placeholder_text="🔍 Filtrar...")
        f_search.pack(fill="x", padx=10, pady=5)
        
        sc = ctk.CTkScrollableFrame(pop)
        sc.pack(fill="both", expand=True, padx=10, pady=10)
        
        def fetch_p():
            data = run_command([ADB, "shell", f"dumpsys package {pkg}"])
            matches = re.findall(r"(android\.permission\.[\w_]+): granted=(true|false)", data)
            current = [(m[0], m[1] == 'true') for m in matches]
            self.update_perm_view(sc, pkg, current, f_search.get())
        
        f_search.bind("<KeyRelease>", lambda e: fetch_p())
        threading.Thread(target=fetch_p, daemon=True).start()

    def update_perm_view(self, sc, pkg, perms, q):
        for w in sc.winfo_children():
            w.destroy()
        for name, state in perms:
            if q.lower() in name.lower():
                f = ctk.CTkFrame(sc)
                f.pack(fill="x", pady=2)
                ctk.CTkLabel(f, text=name, text_color=COLOR_SUCCESS if state else COLOR_DANGER, font=("Consolas", 11)).pack(side="left", padx=5)
                ctk.CTkButton(f, text="Grant", width=60, fg_color="green",
                             command=lambda p=pkg, m=name: run_command([ADB, "shell", "pm", "grant", "--user", "0", p, m])).pack(side="right", padx=2)
                ctk.CTkButton(f, text="Revoke", width=60, fg_color="red",
                             command=lambda p=pkg, m=name: run_command([ADB, "shell", "pm", "revoke", "--user", "0", p, m])).pack(side="right", padx=2)
