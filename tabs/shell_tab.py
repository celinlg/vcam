import customtkinter as ctk
import threading
from utils import run_command, ADB

class ShellTab:
    def __init__(self, parent, after_func):
        self.tab = parent
        self.after_func = after_func
        self.setup_shell_tab()

    def setup_shell_tab(self):
        self.shell_out = ctk.CTkTextbox(self.tab, font=("Consolas", 12))
        self.shell_out.pack(fill="both", expand=True, pady=5)
        
        self.shell_entry = ctk.CTkEntry(self.tab, placeholder_text="adb [comando]...")
        self.shell_entry.pack(fill="x", pady=5)
        self.shell_entry.bind("<Return>", lambda e: self.exec_shell())

    def exec_shell(self):
        cmd = self.shell_entry.get()
        self.shell_entry.delete(0, "end")
        def task():
            result = run_command([ADB] + cmd.split())
            self.after_func(0, lambda: self.shell_out.insert("end", f"\n# adb {cmd}\n" + result))
        threading.Thread(target=task).start()
