import customtkinter as ctk
import threading
import re
from utils import run_command, ADB

class AppsTab:
    def __init__(self, parent, app_cache):
        self.tab = parent
        self.app_cache = app_cache
        self.setup_apps_tab()

    def setup_apps_tab(self):
        h = ctk.CTkFrame(self.tab)
        h.pack(fill="x", padx=10, pady=10)
        
        self.app_search = ctk.CTkEntry(h, placeholder_text="🔍 Filtrar pacotes...", width=300)
        self.app_search.pack(side="left", padx=5)
        self.app_search.bind("<KeyRelease>", self.filter_apps)
        
        self.custom_act = ctk.CTkEntry(h, placeholder_text="Pacote/Activity Custom", width=400)
        self.custom_act.pack(side="left", padx=10)
        
        ctk.CTkButton(h, text="RUN", width=60, command=self.launch_custom).pack(side="left")
        
        self.app_scroll = ctk.CTkScrollableFrame(self.tab)
        self.app_scroll.pack(fill="both", expand=True)

    def filter_apps(self, e):
        q = self.app_search.get().lower()
        self.render_apps([p for p in self.app_cache if q in p.lower()])

    def render_apps(self, lista):
        for w in self.app_scroll.winfo_children():
            w.destroy()
        for p in lista[:100]:
            ctk.CTkButton(self.app_scroll, text=p, anchor="w", fg_color="transparent", border_width=1,
                         command=lambda pkg=p: self.open_intent_window(pkg)).pack(fill="x", pady=1)

    def launch_custom(self):
        t = self.custom_act.get().strip()
        threading.Thread(target=lambda: run_command([ADB, "shell", "am", "start", "--user", "0", "-n", t])).start()

    def open_intent_window(self, pkg):
        pop = ctk.CTkToplevel(self.tab)
        pop.title(f"Intents: {pkg}")
        pop.geometry("750x600")
        pop.attributes("-topmost", True)
        
        sc = ctk.CTkScrollableFrame(pop)
        sc.pack(fill="both", expand=True, padx=10, pady=10)
        
        def fetch():
            data = run_command([ADB, "shell", f"dumpsys package {pkg}"])
            acts = list(set(re.findall(r"[\w\.]+/[\w\.]+", data)))
            for a in acts:
                ctk.CTkButton(sc, text=a, anchor="w", fg_color="transparent", hover_color="#2c3e50", height=35,
                             command=lambda t=a: run_command([ADB, "shell", "am", "start", "--user", "0", "-n", t])).pack(fill="x", pady=1)
        
        threading.Thread(target=fetch, daemon=True).start()
