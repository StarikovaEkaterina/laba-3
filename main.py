import tkinter as tk


class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Менеджер паролей")
        self.geometry("600x400")
        self.minsize(500, 350)


if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()

