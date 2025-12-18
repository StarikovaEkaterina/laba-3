import tkinter as tk
from tkinter import ttk, messagebox


class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Менеджер паролей")
        self.geometry("600x400")
        self.minsize(500, 350)

        self._create_menu()
        self._create_widgets()

    def _create_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)

        menubar.add_cascade(label="Файл", menu=file_menu)
        menubar.add_cascade(label="Справка", menu=help_menu)

        self.config(menu=menubar)

    def _create_widgets(self):
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            frame,
            columns=("service", "login", "password"),
            show="headings"
        )

        self.tree.heading("service", text="Сервис")
        self.tree.heading("login", text="Логин")
        self.tree.heading("password", text="Пароль")

        self.tree.pack(fill=tk.BOTH, expand=True)

    def show_about(self):
        messagebox.showinfo(
            "О программе",
            "Менеджер паролей\nЛабораторная работа (вариант 28)\nPython + Tkinter"
        )


if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
