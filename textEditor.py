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
        self.create_app_menu()

        # Create Toolbar
        self.create_toolbar()

        # Text Area with Scrollbar
        self.create_text_area()

        # Status Bar
        self.create_status_bar()

        # Bind events
        self.text_area.bind("<KeyRelease>", self.on_text_change)
        self.text_area.bind(
            "<Key>", lambda e: self.root.after(10, self.update_all)
        )  # Immediate feedback
        self.text_area.bind("<<Modified>>", self.on_text_change)
        self.text_area.bind("<ButtonRelease-1>", self.on_text_change)

        self.update_all()  # Initialize status bar with correct info

    # ==================== MENU ====================
    def bind_shortcuts(self, key, command):
        self.root.bind(key, lambda e: command())

    def create_app_menu(self):
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
        file_menu.add_command(
            label="Save As...", accelerator="Ctrl+Shift+S", command=self.save_as_file
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit", accelerator="Ctrl+Q", command=self.root.quit
        )

        # =============== BIND THE SHORTCUTS ===============
        self.bind_shortcuts("<Control-n>", self.new_file)
        self.bind_shortcuts("<Control-o>", self.open_file)
        self.bind_shortcuts("<Control-s>", self.save_file)
        self.bind_shortcuts("<Control-S>", self.save_as_file)
        self.bind_shortcuts("<Control-q>", self.root.quit)
        self.bind_shortcuts("<Control-z>", self.edit_undo)
        self.bind_shortcuts("<Control-Z>", self.edit_redo)
        # Shift+Z is not working in some environments, using Ctrl+Shift+Z instead

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
        edit_menu.add_command(
            label="Undo", accelerator="Ctrl+Z", command=self.edit_undo
        )
        edit_menu.add_command(
            label="Redo", accelerator="Ctrl+Shift+Z", command=self.edit_redo
        )

    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, pady=2)

        ttk.Button(toolbar, text="New", command=self.new_file).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(toolbar, text="Open", command=self.open_file).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(toolbar, text="Save", command=self.save_file).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(toolbar, text="Save As", command=self.save_as_file).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        ttk.Button(toolbar, text="Undo", command=self.edit_undo).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(toolbar, text="Redo", command=self.edit_redo).pack(
            side=tk.LEFT, padx=2
        )

    # def create_text_area(self):
    #     # Frame for text area
    #     text_frame = tk.Frame(self.root)
    #     text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    #     # Scrollbar
    #     scrollbar = tk.Scrollbar(text_frame)
    #     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #     # Text Widget
    #     self.text_area = tk.Text(
    #         text_frame, wrap=tk.WORD, undo=True, font=("Consolas", 11)
    #     )
    #     self.text_area.pack(fill=tk.BOTH, expand=True)

    #     # Configure scrollbar
    #     scrollbar.config(command=self.text_area.yview)
    #     self.text_area.config(yscrollcommand=scrollbar.set)

    def create_text_area(self):
        # Main frame
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ==================== LINE NUMBERS ====================
        self.line_numbers = tk.Text(
            text_frame,
            width=4,
            padx=4,
            pady=5,
            takefocus=0,
            bg="#f0f0f0",  # Light gray background
            fg="#666666",
            font=("Consolas", 11),
            state="disabled",
        )
        self.line_numbers.grid(row=0, column=0, sticky="ns")

        # ==================== TEXT AREA + SCROLLBAR ===========
        # Main text area
        self.text_area = tk.Text(
            text_frame, wrap=tk.WORD, undo=True, font=("Consolas", 11)
        )
        self.text_area.grid(row=0, column=1, sticky="nsew")

        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame, width=14)
        scrollbar.grid(row=0, column=2, sticky="ns")

        # Configure grid weights for proper resizing
        text_frame.columnconfigure(1, weight=1)
        text_frame.rowconfigure(0, weight=1)

        # Configure scrollbar for both widgets
        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.on_scroll)

        # ==================== BINDINGS ====================
        self.text_area.bind("<KeyRelease>", self.on_text_change)
        self.text_area.bind("<<Modified>>", self.on_text_change)
        self.text_area.bind("<ButtonRelease-1>", self.on_text_change)
        self.text_area.bind("<MouseWheel>", self.on_scroll)
        self.text_area.bind("<Button-4>", self.on_scroll)  # For Linux scroll up
        self.text_area.bind("<Button-5>", self.on_scroll)  # For Linux scroll down

    def on_scroll(self, *args):
        """Sync scrolling between text area and line numbers."""
        if isinstance(args[0], tk.Event) if args else False:
            fraction = self.text_area.yview()[0]
            self.line_numbers.yview_moveto(fraction)
        else:
            self.text_area.yview(*args)
            self.line_numbers.yview(*args)

    def update_line_numbers(self):
        """Update line numbers based on the current number of lines in the text area."""
        try:
            total_lines = int(self.text_area.index("end-1c").split(".")[0])
            line_numbers_str = "\n".join(str(i) for i in range(1, total_lines + 1))
            self.line_numbers.config(state="normal")
            self.line_numbers.delete("1.0", tk.END)
            self.line_numbers.insert("1.0", line_numbers_str)
            self.line_numbers.config(state="disabled")
        except Exception:
            pass

    def create_status_bar(self):
        self.status_bar = tk.Label(
            self.root,
            text="Ready | Untitled",
            anchor=tk.W,
            relief=tk.SUNKEN,
            padx=5,
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_text_change(self, event=None):
        # Cancel any pending update
        if hasattr(self, "_update_job") and self._update_job:
            self.root.after_cancel(self._update_job)

        self._update_job = self.root.after(80, self.update_all)

    def update_status(self):
        try:
            content = self.text_area.get("1.0", tk.END)
            line_count = int(self.text_area.index("end-1c").split(".")[0])
            word_count = len(content.strip().split()) if content.strip() else 0
            filename = (
                os.path.basename(self.current_file) if self.current_file else "Untitled"
            )

            modified = " | * (Unsaved)" if self.text_area.edit_modified() else ""
            status = f"Lines: {line_count} | Words: {word_count} | {filename}{modified}"
            self.status_bar.config(text=status)

        except Exception:
            self.status_bar.config(text="Lines: 0 | Words: 0 | Untitled")

    def update_all(self):
        self.update_line_numbers()
        self.update_status()

    # ==================== FILE METHODS ====================
    def new_file(self):
        if self.check_unsaved():
            self.text_area.delete("1.0", tk.END)
            self.current_file = None
            self.text_area.edit_modified(False)
            self.update_all()

    def open_file(self):
        if not self.check_unsaved():
            return

        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", content)
                    self.current_file = file_path
                    self.text_area.edit_modified(False)
                    self.update_all()

            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: \n{e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as file:
                    content = self.text_area.get("1.0", tk.END).rstrip("\n")
                    file.write(content)

                self.text_area.edit_modified(False)
                self.update_all()
                messagebox.showinfo("Saved", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: \n{e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    content = self.text_area.get("1.0", tk.END).rstrip("\n")
                    file.write(content)

                self.current_file = file_path
                self.text_area.edit_modified(False)
                self.update_all()
                messagebox.showinfo("Saved", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: \n{e}")

    def edit_undo(self):
        try:
            self.text_area.edit_undo()
            self.update_all()
        except tk.TclError:
            pass  # No more actions to undo

    def edit_redo(self):
        try:
            self.text_area.edit_redo()
            self.update_all()
        except tk.TclError:
            pass  # No more actions to redo

    def check_unsaved(self):
        """Check if there are unsaved changes before performing actions like New or Open."""
        if not self.text_area.edit_modified():
            return True  # No unsaved changes, proceed normally

        response = messagebox.askyesnocancel(
            "Unsaved Changes",
            "You have unsaved changes. Do you want to save them?",
        )
        if response is True:  # Yes - save and proceed only if successful
            self.save_file()  # Check if file was actually saved
            return not self.text_area.edit_modified()  # Still modified = save failed
        elif response is False:  # No - discard changes and proceed
            self.text_area.edit_modified(
                False
            )  # Reset modified flag since we're discarding changes
            return True
        else:  # None - Cancel
            return False


if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
