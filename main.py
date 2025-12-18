import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

DATA_FILE = "passwords.json"

class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Менеджер паролей")
        self.geometry("600x400")
        self.minsize(500, 350)

        self._create_menu()
        self._create_widgets()
        self._load_data()

    def _create_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Сохранить", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)

        menubar.add_cascade(label="Файл", menu=file_menu)
        menubar.add_cascade(label="Справка", menu=help_menu)

        self.config(menu=menubar)

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(main_frame, columns=("service", "login", "password"), show="headings")
        self.tree.heading("service", text="Сервис")
        self.tree.heading("login", text="Логин")
        self.tree.heading("password", text="Пароль")

        self.tree.column("service", width=180)
        self.tree.column("login", width=180)
        self.tree.column("password", width=180)

        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="Добавить", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Изменить", command=self.edit_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_entry).pack(side=tk.LEFT, padx=5)

    def _load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            else:
                self.data = []
            self._refresh_table()
        except (json.JSONDecodeError, IOError) as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            self.data = []

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Сохранение", "Данные успешно сохранены")
        except IOError as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

    def _refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.data:
            self.tree.insert("", tk.END, values=(item["service"], item["login"], item["password"]))

    def add_entry(self):
        try:
            service = simpledialog.askstring("Сервис", "Введите название сервиса:")
            if not service:
                return
            login = simpledialog.askstring("Логин", "Введите логин:")
            password = simpledialog.askstring("Пароль", "Введите пароль:")

            self.data.append({"service": service, "login": login, "password": password})
            self._refresh_table()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def edit_entry(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите запись")
                return

            index = self.tree.index(selected[0])
            item = self.data[index]

            service = simpledialog.askstring("Сервис", "Изменить сервис:", initialvalue=item["service"])
            login = simpledialog.askstring("Логин", "Изменить логин:", initialvalue=item["login"])
            password = simpledialog.askstring("Пароль", "Изменить пароль:", initialvalue=item["password"])

            self.data[index] = {"service": service, "login": login, "password": password}
            self._refresh_table()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_entry(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите запись")
                return

            if messagebox.askyesno("Подтверждение", "Удалить выбранную запись?"):
                index = self.tree.index(selected[0])
                del self.data[index]
                self._refresh_table()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def show_about(self):
        messagebox.showinfo(
            "О программе",
            "Менеджер паролей\n"
            "Лабораторная работа (вариант 28)\n"
            "Язык: Python, GUI: Tkinter"
        )


if __name__ == "__main__":
    try:
        app = PasswordManagerApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Критическая ошибка", str(e))
