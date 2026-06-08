import customtkinter as ctk
import threading
import os
import time
from tkinter import messagebox
from pynput import mouse

from config import (
    ADB, SCRCPY_PATH, WINDOW_WIDTH, WINDOW_HEIGHT,
    COLOR_PURPLE, COLOR_DANGER, COLOR_SUCCESS, COLOR_WARNING, COLOR_INFO
)
from utils import run_command
from tabs.explorer_tab import ExplorerTab
from tabs.shell_tab import ShellTab
from tabs.apps_tab import AppsTab
from tabs.running_tab import RunningTab
from tabs.manage_tab import ManageTab
from tabs.perms_tab import PermsTab
from tabs.monitor_tab import MonitorTab
from tabs.auto_tab import AutoTab


class TitanUltraFinal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔥 TITAN ADB PRO ULTRA - FINAL EDITION 🔥")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.app_cache = []
        self.control_enabled = False

        self.create_top_bar()
        self.create_ui()
        self.start_mouse_listener()
        threading.Thread(target=self.load_apps, daemon=True).start()

    def create_top_bar(self):
        conn_frame = ctk.CTkFrame(self, height=60)
        conn_frame.pack(fill="x", padx=10, pady=5)
        
        self.ip_entry = ctk.CTkEntry(conn_frame, placeholder_text="IP: 192.168.x.x", width=150)
        self.ip_entry.pack(side="left", padx=5)
        
        self.port_entry = ctk.CTkEntry(conn_frame, placeholder_text="5555", width=60)
        self.port_entry.insert(0, "5555")
        self.port_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(conn_frame, text="Conectar", width=80, command=self.connect_wifi).pack(side="left", padx=5)
        ctk.CTkButton(conn_frame, text="ADB USB", fg_color=COLOR_SUCCESS, width=80, command=self.set_adb_usb).pack(side="left", padx=5)
        ctk.CTkButton(conn_frame, text="📱 ESPELHAR", fg_color=COLOR_PURPLE, command=self.start_mirror).pack(side="left", padx=5)
        ctk.CTkButton(conn_frame, text="📸 PRINT", fg_color=COLOR_INFO, command=self.take_screenshot).pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(conn_frame, text="Status: Desconectado", text_color="gray")
        self.status_label.pack(side="right", padx=15)

    def connect_wifi(self):
        target = f"{self.ip_entry.get().strip()}:{self.port_entry.get().strip()}"
        threading.Thread(
            target=lambda: self.status_label.configure(
                text=f"Status: {run_command([ADB, 'connect', target]).strip()}"
            )
        ).start()

    def set_adb_usb(self):
        threading.Thread(
            target=lambda: messagebox.showinfo("USB", run_command([ADB, "usb"]))
        ).start()

    def create_ui(self):
        self.tabs = ctk.CTkTabview(self, command=self.on_tab_change)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tab_explorer = self.tabs.add("📂 Explorer")
        self.tab_shell = self.tabs.add("💻 ADB Shell")
        self.tab_apps = self.tabs.add("🚀 App Launcher")
        self.tab_running = self.tabs.add("🏃 Apps Rodando")
        self.tab_manage = self.tabs.add("📦 Instalar/Desinstalar")
        self.tab_perms = self.tabs.add("🔐 Permissões")
        self.tab_monitor = self.tabs.add("📊 Monitor")
        self.tab_auto = self.tabs.add("⚡ Automação")

        self.explorer_tab = ExplorerTab(self.tab_explorer)
        self.shell_tab = ShellTab(self.tab_shell, self.after)
        self.apps_tab = AppsTab(self.tab_apps, self.app_cache)
        self.running_tab = RunningTab(self.tab_running)
        self.manage_tab = ManageTab(self.tab_manage, self.app_cache)
        self.perms_tab = PermsTab(self.tab_perms, self.app_cache)
        self.monitor_tab = MonitorTab(self.tab_monitor)
        self.auto_tab = AutoTab(self.tab_auto)

        self.ctrl_btn = ctk.CTkButton(self, text="🎮 CONTROLE REMOTO OFF", command=self.toggle_control)
        self.ctrl_btn.pack(pady=10)

    def on_tab_change(self):
        current_tab = self.tabs.get()
        if current_tab in ["🚀 App Launcher", "🔐 Permissões", "📦 Instalar/Desinstalar"] and not self.app_cache:
            self.load_apps()

    def load_apps(self):
        def task():
            out = run_command([ADB, "shell", "pm list packages --user 0"])
            self.app_cache = sorted([p.replace("package:", "").strip() for p in out.splitlines() if "package:" in p])
            self.after(0, lambda: self.update_all_app_tabs())
        threading.Thread(target=task, daemon=True).start()

    def update_all_app_tabs(self):
        self.apps_tab.render_apps(self.app_cache)
        self.perms_tab.render_perms_list(self.app_cache)
        self.manage_tab.update_list()

    def start_mirror(self):
        if os.path.exists(SCRCPY_PATH):
            threading.Thread(target=lambda: run_command([SCRCPY_PATH, "--always-on-top"]), daemon=True).start()
        else:
            messagebox.showerror("Erro", f"Scrcpy não encontrado em: {SCRCPY_PATH}")

    def take_screenshot(self):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        filepath = os.path.join(desktop, f"shot_{int(time.time())}.png")
        
        def screenshot_task():
            run_command([ADB, "shell", "screencap -p /sdcard/s.png"])
            run_command([ADB, "pull", "/sdcard/s.png", filepath])
            messagebox.showinfo("Sucesso", f"Salvo no Desktop: {filepath}")
        
        threading.Thread(target=screenshot_task).start()

    def toggle_control(self):
        self.control_enabled = not self.control_enabled
        text = "🎮 CONTROLE ON" if self.control_enabled else "🎮 CONTROLE OFF"
        color = "red" if self.control_enabled else "#3b8ed0"
        self.ctrl_btn.configure(text=text, fg_color=color)

    def start_mouse_listener(self):
        def on_click(x, y, button, pressed):
            if pressed and self.control_enabled:
                threading.Thread(
                    target=lambda: run_command([ADB, "shell", "input", "tap", str(int(x)), str(int(y))])
                ).start()
        
        mouse.Listener(on_click=on_click).start()


if __name__ == "__main__":
    app = TitanUltraFinal()
    app.mainloop()
