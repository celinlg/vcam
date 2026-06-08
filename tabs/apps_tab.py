import customtkinter as ctk
import threading
import re
from utils import run_command, ADB

class AppsTab:
    def __init__(self, parent, app_cache, user_selector):
        self.tab = parent
        self.app_cache = app_cache
        self.user_selector = user_selector
        self.setup_apps_tab()

    def setup_apps_tab(self):
        self.app_search = ctk.CTkEntry(self.tab, placeholder_text="🔎 Buscar app...")
        self.app_search.pack(fill="x", padx=15, pady=5)
        self.app_search.bind("<KeyRelease>", self.filter_apps)
        
        self.apps_scroll = ctk.CTkScrollableFrame(self.tab)
        self.apps_scroll.pack(fill="both", expand=True)

    def filter_apps(self, event=None):
        query = self.app_search.get().lower()
        filtered = [p for p in self.app_cache if query in p.lower()]
        self.render_app_list(filtered)

    def render_app_list(self, lista_custom=None):
        lista = lista_custom if lista_custom is not None else self.app_cache
        for w in self.apps_scroll.winfo_children():
            w.destroy()
        for p in lista:
            ctk.CTkButton(self.apps_scroll, text=p, anchor="w", fg_color="transparent",
                         command=lambda pkg=p: self.open_activity_selector(pkg)).pack(fill="x")

    def open_activity_selector(self, pkg):
        win = ctk.CTkToplevel(self.tab)
        win.title(pkg)
        win.geometry("600x500")
        win.attributes("-topmost", True)
        scroll = ctk.CTkScrollableFrame(win)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        out = run_command([ADB, "shell", f"dumpsys package {pkg} | grep -E 'Activity'"])
        acts = re.findall(f"{pkg}/[\\w\\.]+", out)
        for a in set(acts):
            ctk.CTkButton(scroll, text=a.split("/")[-1], anchor="w",
                         command=lambda x=a: run_command([ADB, "shell", "am", "start", "-n", x])).pack(fill="x")
