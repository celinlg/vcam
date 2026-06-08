import customtkinter as ctk
import threading
import time
from utils import run_command, ADB

class MonitorTab:
    def __init__(self, parent):
        self.tab = parent
        self.monitoring = False
        self.setup_monitor_tab()

    def setup_monitor_tab(self):
        self.m_box = ctk.CTkTextbox(self.tab, font=("Consolas", 11))
        self.m_box.pack(fill="both", expand=True)
        
        ctk.CTkButton(self.tab, text="▶ Start", command=self.start_monitor).pack(pady=5)
        ctk.CTkButton(self.tab, text="⏹ Stop", command=self.stop_monitor).pack(pady=5)

    def start_monitor(self):
        if self.monitoring:
            return
        self.monitoring = True
        def loop():
            while self.monitoring:
                cpu = run_command([ADB, "shell", "top -n 1 -b | head -10"])
                self.tab.after(0, lambda: (self.m_box.delete("1.0", "end"), self.m_box.insert("end", cpu)))
                time.sleep(3)
        threading.Thread(target=loop, daemon=True).start()

    def stop_monitor(self):
        self.monitoring = False
