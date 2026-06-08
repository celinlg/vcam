import customtkinter as ctk
from tkinter import filedialog
import threading
import os
from utils import run_command, ADB
from config import COLOR_DIRECTORY, COLOR_FILE

class ExplorerTab:
    def __init__(self, parent):
        self.tab = parent
        self.explorer_path = "/sdcard"
        self.selected_item = None
        self.setup_explorer_tab()

    def setup_explorer_tab(self):
        self.path_label = ctk.CTkLabel(self.tab, text=self.explorer_path, font=("Consolas", 14))
        self.path_label.pack(pady=5)
        
        self.explorer_scroll = ctk.CTkScrollableFrame(self.tab)
        self.explorer_scroll.pack(fill="both", expand=True)
        
        f = ctk.CTkFrame(self.tab)
        f.pack(fill="x", pady=5)
        ctk.CTkButton(f, text="⬅ Up", width=80, command=self.explorer_up).pack(side="left", padx=5)
        ctk.CTkButton(f, text="🔄 Refresh", width=80, command=self.explorer_refresh).pack(side="left", padx=5)
        ctk.CTkButton(f, text="⬇ PULL", fg_color="#e67e22", command=self.pull_file).pack(side="right", padx=5)
        ctk.CTkButton(f, text="⬆ PUSH", fg_color="#27ae60", command=self.push_file).pack(side="right", padx=5)

    def explorer_refresh(self):
        out = run_command([ADB, "shell", f"ls -ap {self.explorer_path}"])
        items = [i.strip() for i in out.splitlines() if i.strip() and i not in ["./", "../"]]
        for w in self.explorer_scroll.winfo_children():
            w.destroy()
        for i in items:
            is_dir = i.endswith("/")
            c = COLOR_DIRECTORY if is_dir else COLOR_FILE
            ctk.CTkButton(self.explorer_scroll, text=i, anchor="w", fg_color="transparent", text_color=c,
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
        if self.selected_item:
            d = filedialog.askdirectory()
            if d:
                threading.Thread(target=lambda: run_command([ADB, "pull", f"{self.explorer_path}/{self.selected_item}", d])).start()

    def push_file(self):
        f = filedialog.askopenfilename()
        if f:
            threading.Thread(target=lambda: (run_command([ADB, "push", f, self.explorer_path]), self.explorer_refresh())).start()
