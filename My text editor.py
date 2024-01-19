import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.text_widget = tk.Text(self.root, wrap="word", undo=True)
        self.text_widget.pack(expand=True, fill="both")

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.destroy)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)

        # Format menu
        self.format_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Change Background Color", command=self.change_bg_color)

        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Toggle Line Numbers", command=self.toggle_line_numbers)

    def new_file(self):
        self.text_widget.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)
            self.root.title(f"Text Editor - {file_path}")

    def save_file(self):
        if self.root.title().startswith("Text Editor - "):
            file_path = self.root.title()[15:]
            with open(file_path, "w") as file:
                file.write(self.text_widget.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_widget.get(1.0, tk.END))
            self.root.title(f"Text Editor - {file_path}")

    def undo(self):
        try:
            self.text_widget.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text_widget.edit_redo()
        except tk.TclError:
            pass

    def cut(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste(self):
        self.text_widget.event_generate("<<Paste>>")

    def select_all(self):
        self.text_widget.tag_add("sel", "1.0", tk.END)

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        self.text_widget.config(bg=color)

    def toggle_line_numbers(self):
        current_tags = self.text_widget.tag_names()
        if "linenumbers" in current_tags:
            self.text_widget.tag_remove("linenumbers", "1.0", tk.END)
        else:
            self.text_widget.tag_add("linenumbers", "1.0", tk.END)
            self.update_line_numbers()

    def update_line_numbers(self, event=None):
        current_tags = self.text_widget.tag_names()
        if "linenumbers" in current_tags:
            lines = self.text_widget.get("1.0", tk.END).count("\n")
            line_numbers = "\n".join(str(i) for i in range(1, lines + 1))
            self.text_widget.tag_configure("linenumbers", justify="right")
            self.text_widget.tag_configure("linenumbers", font=("Arial", 12))
            self.text_widget.tag_add("linenumbers", "1.0", tk.END)
            self.text_widget.insert("1.0", f"{line_numbers}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.geometry("800x600")
    root.mainloop()
