import customtkinter as ctk
import threading
import os
from tkinter import messagebox

from config import ADB, SCRCPY_PATH, WINDOW_WIDTH, WINDOW_HEIGHT
from utils import run_command
from tabs.explorer_tab import ExplorerTab
from tabs.shell_tab import ShellTab
from tabs.apps_tab import AppsTab
from tabs.running_tab import RunningTab
from tabs.manage_tab import ManageTab
from tabs.monitor_tab import MonitorTab
from tabs.dsu_tab import DSUTab


class TitanUltraFinal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔥 TITAN ADB PRO ULTRA - V5 🔥")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.app_cache = []
        self.explorer_path = "/sdcard"

        self.create_top_bar()
        self.create_ui()
        threading.Thread(target=self.load_apps, daemon=True).start()
        threading.Thread(target=self.explorer_tab.explorer_refresh, daemon=True).start()

    def create_top_bar(self):
        conn_frame = ctk.CTkFrame(self, height=70)
        conn_frame.pack(fill="x", padx=10, pady=5)
        
        self.ip_entry = ctk.CTkEntry(conn_frame, placeholder_text="IP:Porta", width=140)
        self.ip_entry.pack(side="left", padx=5)
        ctk.CTkButton(conn_frame, text="Conectar", width=80, command=self.connect_wifi).pack(side="left", padx=2)
        
        ctk.CTkLabel(conn_frame, text="USUÁRIO:").pack(side="left", padx=(20, 5))
        self.user_selector = ctk.CTkComboBox(conn_frame, values=["0", "10", "11", "999"], width=70)
        self.user_selector.set("0")
        self.user_selector.pack(side="left", padx=5)
        
        ctk.CTkButton(conn_frame, text="📱 ESPELHAR (LOW LATENCY)", fg_color="#8e44ad", command=self.start_mirror).pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(conn_frame, text="Status: Pronto", text_color="gray")
        self.status_label.pack(side="right", padx=15)

    def connect_wifi(self):
        t = self.ip_entry.get().strip()
        self.status_label.configure(text="Conectando...", text_color="yellow")
        threading.Thread(target=lambda: self.status_label.configure(text=f"Status: {run_command([ADB, 'connect', t]).strip()}")).start()

    def create_ui(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=5)
        
        tab_explorer = self.tabs.add("📂 Explorer")
        tab_running = self.tabs.add("🏃 Apps Rodando")
        tab_apps = self.tabs.add("🚀 App Launcher")
        tab_manage = self.tabs.add("📦 Gerenciar")
        tab_monitor = self.tabs.add("📊 Monitor")
        tab_dsu = self.tabs.add(⚡ DSU Manager")
        tab_shell = self.tabs.add("💻 ADB Shell")

        self.explorer_tab = ExplorerTab(tab_explorer, self.update_status)
        self.running_tab = RunningTab(tab_running)
        self.apps_tab = AppsTab(tab_apps, self.app_cache, self.user_selector)
        self.manage_tab = ManageTab(tab_manage, self.app_cache, self.user_selector, self.load_apps)
        self.manage_tab.set_status_callback(self.status_label)
        self.monitor_tab = MonitorTab(tab_monitor)
        self.dsu_tab = DSUTab(tab_dsu)
        self.shell_tab = ShellTab(tab_shell)

    def update_status(self, text, color="gray"):
        self.status_label.configure(text=f"Status: {text}", text_color=color)

    def load_apps(self):
        u = self.user_selector.get()
        self.status_label.configure(text=f"Lendo apps do usuário {u}...", text_color="yellow")
        
        def task():
            out = run_command([ADB, "shell", "pm", "list", "packages", "--user", u, "-3"])
            self.app_cache = sorted([line.replace("package:", "").strip() for line in out.splitlines() if line.strip()])
            
            self.after(0, lambda: [
                self.apps_tab.render_app_list(),
                self.manage_tab.render_manage_list(),
                self.status_label.configure(text="Apps Sincronizados", text_color="green")
            ])
        threading.Thread(target=task, daemon=True).start()

    def start_mirror(self):
        if os.path.exists(SCRCPY_PATH):
            threading.Thread(target=lambda: run_command([SCRCPY_PATH, "--max-size=800", "--video-bit-rate=2M", "--max-fps=15", "--no-audio", "-S"]), daemon=True).start()
        else:
            messagebox.showerror("Erro", f"Scrcpy não encontrado em: {SCRCPY_PATH}")


if __name__ == "__main__":
    TitanUltraFinal().mainloop()
