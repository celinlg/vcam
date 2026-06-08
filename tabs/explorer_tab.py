import customtkinter as ctk
from tkinter import filedialog
import threading
import os
from utils import run_command, ADB
from config import COLOR_DIRECTORY, COLOR_FILE

class ExplorerTab:
    def __init__(self, parent, status_callback):
        self.tab = parent
        self.status_callback = status_callback
        self.explorer_path = "/sdcard"
        self.selected_item = None
        self.setup_explorer_tab()

    def setup_explorer_tab(self):
        self.path_label = ctk.CTkLabel(self.tab, text=self.explorer_path, font=("Consolas", 14))
        self.path_label.pack(pady=5)
        
        self.explorer_scroll = ctk.CTkScrollableFrame(self.tab)
        self.explorer_scroll.pack(fill="both", expand=True)
        
        self.prog_bar = ctk.CTkProgressBar(self.tab, width=700)
        self.prog_bar.set(0)
        self.prog_bar.pack(pady=10)
        
        f = ctk.CTkFrame(self.tab)
        f.pack(fill="x", pady=5)
        ctk.CTkButton(f, text="⬅ Up", command=self.explorer_up).pack(side="left", padx=5)
        ctk.CTkButton(f, text="🔄 Refresh", command=self.explorer_refresh).pack(side="left", padx=5)
        ctk.CTkButton(f, text="⬇ PULL", fg_color="#e67e22", command=self.pull_file).pack(side="right", padx=5)
        ctk.CTkButton(f, text="⬆ PUSH", fg_color="#27ae60", command=self.push_file).pack(side="right", padx=5)

    def explorer_refresh(self):
        def task():
            out = run_command([ADB, "shell", f"ls -ap {self.explorer_path}"])
            items = [i.strip() for i in out.splitlines() if i.strip() and i not in ["./", "../"]]
            # Usar after para atualizar na thread principal
            self.tab.after(0, lambda: self.render_explorer(items))
        threading.Thread(target=task, daemon=True).start()

    def render_explorer(self, items):
        for w in self.explorer_scroll.winfo_children():
            w.destroy()
        for i in items:
            is_dir = i.endswith("/")
            ctk.CTkButton(self.explorer_scroll, text=i, anchor="w", fg_color="transparent",
                         text_color=COLOR_DIRECTORY if is_dir else COLOR_FILE,
                         command=lambda n=i.rstrip("/"), d=is_dir: self.on_item_click(n, d)).pack(fill="x")

    def on_item_click(self, n, d):
        if d:
            self.explorer_path = f"{self.explorer_path.rstrip('/')}/{n}"
            self.path_label.configure(text=self.explorer_path)
            self.explorer_refresh()
        else:
            self.selected_item = n

    def explorer_up(self):
        if self.explorer_path != "/":
            self.explorer_path = os.path.dirname(self.explorer_path.rstrip("/")) or "/"
            self.path_label.configure(text=self.explorer_path)
            self.explorer_refresh()

    def pull_file(self):
        if not hasattr(self, 'selected_item'):
            return
        d = filedialog.askdirectory()
        if d:
            self.prog_bar.set(0.2)
            threading.Thread(target=lambda: (run_command([ADB, "pull", f"{self.explorer_path}/{self.selected_item}", d]), 
                                            self.tab.after(0, lambda: self.prog_bar.set(1)))).start()

    def push_file(self):
        f = filedialog.askopenfilename()
        if f:
            self.prog_bar.set(0.2)
            self.status_callback("Enviando...")
            threading.Thread(target=lambda: (run_command([ADB, "push", f, self.explorer_path]), 
                                            self.tab.after(0, lambda: [self.prog_bar.set(1), self.explorer_refresh(), 
                                                                       self.status_callback("Concluído")]))).start()
