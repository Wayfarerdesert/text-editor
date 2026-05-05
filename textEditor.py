import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("900x600")

        # Current file path
        self.current_file = None

        # Create Menu
        self.app_menu()

        # Create Toolbar
        self.toolbar()

        # Text Area with Scrollbar
        self.text_area()

        # Status Bar
        self.status_bar()

        # Bind events
        self.text_area.bind("<<Modified>>", self.on_text_change)

    # ==================== MENU ====================
    def app_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(
            label="Open...", accelerator="Ctrl+O", command=self.open_file
        )
        file_menu.add_command(
            label="Save", accelerator="Ctrl+S", command=self.save_file
        )
        file_menu.add_command(label="Save As...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(
            label="Cut",
            accelerator="Ctrl+X",
            command=lambda: self.text_area.event_generate("<<Cut>>"),
        )
        edit_menu.add_command(
            label="Copy",
            accelerator="Ctrl+C",
            command=lambda: self.text_area.event_generate("<<Copy>>"),
        )
        edit_menu.add_command(
            label="Paste",
            accelerator="Ctrl+V",
            command=lambda: self.text_area.event_generate("<<Paste>>"),
        )

    def toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, pady=2)

        ttk.Button(toolbar, text="New", command=self.new_file).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(toolbar, text="Open", command=self.open_file).pack(
            side=tk.LEFT, padx=2
        )

    def text_area(self):
        # Frame for text area
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text Widget
        self.text_area = tk.Text(
            text_frame, wrap=tk.WORD, undo=True, font=("Consolas", 11)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Configure scrollbar
        scrollbar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=scrollbar.set)

    def status_bar(self):
        self.status_bar = tk.Label(
            self.root,
            text="Ready | Untitled",
            anchor=tk.W,
            relief=tk.SUNKEN,
            padx=5,
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_text_change(self, event=None):
        self.text_area.edit_modified(False)
        self.update_status()

    def update_status(self):
        words = len(self.text_area.get("1.0", tk.END).split())
        status = f"Words: {words} | "
        if self.current_file:
            status += os.path.basename(self.current_file)
        else:
            status += "Untitled"
        self.status_bar.config(text=status)

    # ==================== FILE METHODS ====================
    def new_file(self):
        if self.check_unsaved():
            self.text_area.delete("1.0", tk.END)
            self.current_file = None
            # self.update_status

    def open_file(self):
        pass

    def save_file(self):
        pass

    def save_as_file(self):
        pass

    def check_unsaved(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
