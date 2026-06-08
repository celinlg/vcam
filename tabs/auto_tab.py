import customtkinter as ctk
import threading
from utils import run_command, ADB

class AutoTab:
    def __init__(self, parent):
        self.tab = parent
        self.setup_auto_tab()

    def setup_auto_tab(self):
        f = ctk.CTkFrame(self.tab)
        f.pack(pady=20)
        
        ctk.CTkButton(f, text="⚡ Gamer Mode", command=self.enable_gamer_mode).pack(pady=10)
        ctk.CTkButton(f, text="🧹 Force Stop Apps", command=self.force_stop_apps).pack(pady=10)

    def enable_gamer_mode(self):
        threading.Thread(target=lambda: run_command([ADB, "shell", "settings put global animator_duration_scale 0"])).start()

    def force_stop_apps(self):
        apps_to_stop = ["com.facebook.katana", "com.instagram.android"]
        for app in apps_to_stop:
            threading.Thread(target=lambda a=app: run_command([ADB, "shell", f"am force-stop --user 0 {a}"])).start()
