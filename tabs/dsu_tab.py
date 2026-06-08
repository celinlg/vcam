import customtkinter as ctk
from tkinter import messagebox
import threading
from utils import run_command, ADB

class DSUTab:
    def __init__(self, parent):
        self.tab = parent
        self.setup_dsu_tab()

    def setup_dsu_tab(self):
        self.dsu_status = ctk.CTkTextbox(self.tab, font=("Consolas", 12), height=200)
        self.dsu_status.pack(fill="x", padx=20, pady=20)
        
        btn_frame = ctk.CTkFrame(self.tab)
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="🔍 Verificar Status DSU", command=self.check_dsu).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="✅ Ativar DSU (Sticky)", fg_color="#27ae60", command=self.enable_dsu_sticky).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="❌ Voltar ao Nativo", fg_color="#e74c3c", command=self.disable_dsu).pack(side="left", padx=10)
        
        ctk.CTkLabel(self.tab, text="Nota: 'Sticky' faz o sistema sempre ligar no DSU.\nVoltar ao nativo exclui os dados temporários do DSU.", text_color="gray").pack(pady=20)

    def check_dsu(self):
        res = run_command([ADB, "shell", "gsi_tool status"])
        self.dsu_status.delete("1.0", "end")
        self.dsu_status.insert("end", f"ESTADO ATUAL DO DSU:\n\n{res}")

    def enable_dsu_sticky(self):
        if messagebox.askyesno("Confirmar", "Deseja forçar o boot pelo DSU (Sticky)?\nO aparelho irá reiniciar."):
            threading.Thread(target=lambda: [
                run_command([ADB, "shell", "gsi_tool enable -s"]),
                run_command([ADB, "reboot"])
            ]).start()

    def disable_dsu(self):
        if messagebox.askyesno("Confirmar", "Deseja desativar o DSU e voltar ao sistema nativo?"):
            threading.Thread(target=lambda: [
                run_command([ADB, "shell", "gsi_tool disable"]),
                run_command([ADB, "shell", "gsi_tool wipe"]),
                run_command([ADB, "reboot"])
            ]).start()
