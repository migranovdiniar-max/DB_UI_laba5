import tkinter as tk
from tkinter import ttk

# подключаем все UI-модули
from app.ui.ui_topic import TopicWindow
from app.ui.ui_grammar import GrammarWindow
from app.ui.ui_vocabulary import VocabularyWindow
from app.ui.ui_exercise import ExerciseWindow
from app.ui.ui_exercise_answer import ExerciseAnswerWindow
from app.ui.ui_user_answers import UserExerciseWindow
from app.ui.ui_users import UsersWindow
from app.ui.ui_definition import DefinitionWindow


class MainWindow:
    def __init__(self, user):
        self.user = user
        self.win = tk.Tk()
        self.win.title(f"Main Menu - {user['role']}")
        self.win.geometry("500x500")

        title = tk.Label(self.win, text="Main Menu", font=("Arial", 18, "bold"))
        title.pack(pady=15)

        frame = tk.Frame(self.win)
        frame.pack(expand=True)

        # Создаём кнопки
        buttons = [
            ("Topics", self.open_topics),
            ("Grammar Rules", self.open_grammar),
            ("Vocabulary", self.open_vocabulary),
            ("Definition", self.open_definition),
            ("Exercises", self.open_exercises),
            ("Exercise Answers", self.open_exercise_answers),
            ("User Answers", self.open_user_answers),
            ("Users", self.open_users)
        ]

        for text, cmd in buttons:
            tk.Button(frame, text=text, width=25, height=2, command=cmd)\
                .pack(pady=6)

        self.win.mainloop()

    def open_topics(self):
        TopicWindow()

    def open_grammar(self):
        GrammarWindow()

    def open_vocabulary(self):
        VocabularyWindow()

    def open_definition(self):
        DefinitionWindow()

    def open_exercises(self):
        ExerciseWindow()

    def open_exercise_answers(self):
        ExerciseAnswerWindow()

    def open_user_answers(self):
        UserExerciseWindow(self.user)

    def open_users(self):
        UsersWindow()
