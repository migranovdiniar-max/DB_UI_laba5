import tkinter as tk
from tkinter import messagebox
from app.auth import authenticate
from app.ui.ui_main import MainWindow


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Авторизация — English App")
        self.root.geometry("3320x180")

        tk.Label(self.root, text="Email").pack(pady=(10, 0))
        self.email = tk.Entry(self.root)
        self.email.pack()

        tk.Label(self.root, text="Password").pack(pady=(8, 0))
        self.password = tk.Entry(self.root, show="*")
        self.password.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(
            pady=12
        )
        self.root.mainloop()

    def login(self):
        email = self.email.get().strip()
        password = self.password.get().strip()
        user = authenticate(email, password)

        if user:
            self.root.destroy()
            MainWindow(user)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")