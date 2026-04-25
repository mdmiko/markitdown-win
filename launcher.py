import os
import subprocess
import customtkinter as ctk
import tkinter as tk # Fondamentale per il fix
from tkinter import messagebox, filedialog, Menu
from tkinterdnd2 import DND_FILES, TkinterDnD
import re
import threading
import webbrowser

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MarkitdownLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("MarkItDown Suite")
        self.root.geometry("600x260")
        self.root.resizable(False, False)
        
        # Stato impostazioni
        self.settings = {
            "api_key": "",
            "model": "gpt-4o",
            "always_on_top": False,
            "debug": False
        }
        self.is_processing = False
        self.settings_win = None

        self._setup_menu()
        self._setup_main_ui()

    def _setup_menu(self):
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        
        file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open & Convert...", command=self.select_files_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        self.menubar.add_command(label="Settings", command=self.open_settings)
        
        help_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def _setup_main_ui(self):
        self.drop_frame = ctk.CTkFrame(self.root, corner_radius=15, border_width=2, border_color="#3B8ED0")
        self.drop_frame.pack(pady=15, padx=20, fill="both", expand=True)
        
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.handle_drop)
        
        self.label = ctk.CTkLabel(
            self.drop_frame, 
            text="Drag & Drop files here or click to browse", 
            font=ctk.CTkFont(size=16, weight="bold"),
            cursor="hand2"
        )
        self.label.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.drop_frame.bind("<Button-1>", lambda e: self.select_files_dialog())
        self.label.bind("<Button-1>", lambda e: self.select_files_dialog())
        
        self.status_label = ctk.CTkLabel(self.root, text="Status: Ready", font=ctk.CTkFont(size=11), wraplength=550)
        self.status_label.pack(pady=(0, 10))

    def show_about(self):
        about_msg = "MarkItDown Suite v0.4\n\nGUI for Microsoft's MarkItDown CLI.\nLicense: MIT"
        if messagebox.askyesno("About", f"{about_msg}\n\nVisit GitHub project?"):
            webbrowser.open("https://github.com/microsoft/markitdown")

    def open_settings(self):
        """Fix definitivo: usa tk.Toplevel invece di ctk.CTkToplevel per evitare il bug della trasparenza."""
        if self.settings_win is not None and self.settings_win.winfo_exists():
            self.settings_win.focus()
            return

        # Usiamo il Toplevel standard di Tkinter
        self.settings_win = tk.Toplevel(self.root)
        self.settings_win.title("Settings")
        self.settings_win.geometry("450x420")
        self.settings_win.resizable(False, False)
        self.settings_win.attributes("-topmost", True)
        
        # Impostiamo lo sfondo per farlo sembrare un CTk
        bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1] if ctk.get_appearance_mode() == "Dark" else ctk.ThemeManager.theme["CTkFrame"]["fg_color"][0]
        self.settings_win.configure(bg=bg_color)

        container = ctk.CTkFrame(self.settings_win)
        container.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(container, text="AI Configurations", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=15)
        
        entry_key = ctk.CTkEntry(container, width=350, placeholder_text="OpenAI API Key", show="*")
        entry_key.insert(0, self.settings["api_key"])
        entry_key.pack(pady=10)

        entry_model = ctk.CTkEntry(container, width=350, placeholder_text="Model (eg. gpt-4o)")
        entry_model.insert(0, self.settings["model"])
        entry_model.pack(pady=10)

        sw_debug = ctk.CTkSwitch(container, text="Enable Debug Logs")
        if self.settings["debug"]: sw_debug.select()
        sw_debug.pack(pady=10, padx=20, anchor="w")

        sw_top = ctk.CTkSwitch(container, text="Always on Top")
        if self.settings["always_on_top"]: sw_top.select()
        sw_top.pack(pady=10, padx=20, anchor="w")

        def save():
            self.settings.update({
                "api_key": entry_key.get(),
                "model": entry_model.get(),
                "debug": sw_debug.get(),
                "always_on_top": sw_top.get()
            })
            self.root.attributes("-topmost", self.settings["always_on_top"])
            self.settings_win.destroy()

        ctk.CTkButton(container, text="Save Settings", command=save).pack(pady=20)

    def handle_drop(self, event):
        if self.is_processing: return
        data = event.data
        files = re.findall(r'\{(.*?)\}', data) if '{' in data else data.split()
        self.start_conversion_thread(files)

    def select_files_dialog(self):
        if self.is_processing: return
        files = filedialog.askopenfilenames(title="Select files")
        if files:
            self.start_conversion_thread(list(files))

    def start_conversion_thread(self, file_list):
        self.is_processing = True
        threading.Thread(target=self._process_files_worker, args=(file_list,), daemon=True).start()

    def _process_files_worker(self, file_list):
        engine = "markitdown-cli.exe"
        if not os.path.exists(engine):
            self.root.after(0, lambda: messagebox.showerror("Error", "markitdown-cli.exe not found."))
            self.is_processing = False
            return

        total = len(file_list)
        success = 0

        for i, f_path in enumerate(file_list):
            f_path = f_path.strip()
            name = os.path.basename(f_path)
            self.root.after(0, lambda n=name, idx=i+1: self.status_label.configure(
                text=f"Converting {idx}/{total}: {n}", text_color="#3B8ED0"))

            cmd = [engine, f_path]
            if self.settings["api_key"]:
                cmd.extend(["--key", self.settings["api_key"], "--model", self.settings["model"]])
            if self.settings["debug"]:
                cmd.append("--debug")
            
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
                if res.returncode == 0: success += 1
            except Exception: pass

        self.is_processing = False
        self.root.after(0, lambda: self.status_label.configure(
            text=f"Done: {success}/{total} successful", text_color="#2FA572"))
        self.root.after(0, lambda: messagebox.showinfo("Completed", f"Processed {total} files."))

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.attributes("-alpha", 1.0)
    app = MarkitdownLauncher(root)
    root.mainloop()