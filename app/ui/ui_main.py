import tkinter as tk
from app.ui.ui_vocabulary import VocabularyWindow 


class MainWindow:
    def __init__(self, user: dict):
        self.user = user
        self.root = tk.Tk()
        self.root.title(f"English App — {user['role']} — {user['name']}")
        self.root.geometry("600x400")

        tk.Label(self.root, text=f"Welcome, {user['name']} ({user['role']})", font=("Arial", 14)).pack(pady=10)

        if user["role"] in ("admin", "teacher"):
            btn_ex = tk.Button(self.root, text="Exercises (manage)", command=self.open_exercises)
            btn_ex.pack(fill="x", padx=20, pady=5)

        if user["role"] in ("admin", "teacher"):
            btn_users = tk.Button(self.root, text="Users (manage)", command=self.open_users)
            btn_users.pack(fill="x", padx=20, pady=5)

        btn_vocab = tk.Button(self.root, 
                              text="Vocabulary", 
                              command=self.open_vocabulary)
        btn_vocab.pack(fill="x", padx=20, pady=5)

        btn_exit = tk.Button(self.root, text="Exit", command=self.root.destroy)
        btn_exit.pack(side="bottom", pady=10)

        self.root.mainloop()

        def open_vocabulary(self):
            from app.ui.ui_vocabulary import VocabularyWindow
            VocabularyWindow()

        def open_user(self):
            from app.ui.ui_users import UserWindow
            UserWindow()

        def open_exercises(self):
            from app.ui.ui_exercise import ExerciseWindow
            ExerciseWindow()


from app.ui.ui_login import LoginWindow

if __name__ == "__main__":
    LoginWindow()
