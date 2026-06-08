import customtkinter as ctk
import threading
from utils import run_command, ADB
from config import COLOR_DANGER

class RunningTab:
    def __init__(self, parent):
        self.tab = parent
        self.setup_running_tab()

    def setup_running_tab(self):
        f = ctk.CTkFrame(self.tab)
        f.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(f, text="🔄 Atualizar Processos", command=self.list_running).pack(side="left")
        
        self.run_scroll = ctk.CTkScrollableFrame(self.tab)
        self.run_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    def list_running(self):
        def task():
            out = run_command([ADB, "shell", "ps -A | grep u0_a"])
            self.render_running(out.splitlines())
        threading.Thread(target=task, daemon=True).start()

    def render_running(self, lines):
        for w in self.run_scroll.winfo_children():
            w.destroy()
        for line in lines:
            parts = line.split()
            if len(parts) < 9:
                continue
            pkg = parts[-1]
            row = ctk.CTkFrame(self.run_scroll)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=pkg, anchor="w").pack(side="left", padx=10, expand=True, fill="x")
            ctk.CTkButton(row, text="Finalizar", width=80, fg_color=COLOR_DANGER,
                         command=lambda p=pkg: self.kill_app(p)).pack(side="right", padx=5)

    def kill_app(self, pkg):
        threading.Thread(target=lambda: (run_command([ADB, "shell", f"am force-stop {pkg}"]), self.list_running())).start()
