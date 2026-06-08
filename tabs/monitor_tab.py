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
        
        self.start_btn = ctk.CTkButton(self.tab, text="▶ Start", command=self.start_monitor)
        self.start_btn.pack(pady=5)
        
        self.stop_btn = ctk.CTkButton(self.tab, text="⏹ Stop", command=self.stop_monitor)
        self.stop_btn.pack(pady=5)

    def start_monitor(self):
        if not self.monitoring:
            self.monitoring = True
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            
            def loop():
                while self.monitoring:
                    cpu = run_command([ADB, "shell", "top -n 1 -b | head -10"])
                    self.m_box.delete("1.0", "end")
                    self.m_box.insert("end", cpu)
                    time.sleep(3)
            
            threading.Thread(target=loop, daemon=True).start()

    def stop_monitor(self):
        self.monitoring = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
