import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from app.db import get_connection

class ExerciseWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Exercises")
        self.win.geometry("700x400")

        self.tree = ttk.Treeview(self.win, columns=("problem","type","level","topic_id"), show="headings")
        for col, title in [("problem","Problem"), ("type","Type"), ("level","Level"), ("topic_id","Topic ID")]:
            self.tree.heading(col, text=title)
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True)

        frame = tk.Frame(self.win)
        frame.pack(fill="x", pady=6)
        tk.Button(frame, text="Add", command=self.add_exercise).pack(side="left", padx=5)
        tk.Button(frame, text="Edit", command=self.edit_exercise).pack(side="left", padx=5)
        tk.Button(frame, text="Delete", command=self.delete_exercise).pack(side="left", padx=5)
        tk.Button(frame, text="Refresh", command=self.load_data).pack(side="left", padx=5)

        self.load_data()

    def load_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT exercise_id, problem, type, exercise_level, topic_id FROM exercise")
        for row in cur.fetchall():
            self.tree.insert("", "end", iid=row["exercise_id"], values=(row["problem"], row["type"], row["exercise_level"], row["topic_id"]))
        conn.close()

    def add_exercise(self):
        dlg = AddEditExercise(self.win)
        self.win.wait_window(dlg.top)
        if dlg.result:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO exercise (problem,type,exercise_level,topic_id) VALUES (?, ?, ?, ?)",
                        (dlg.result["problem"], dlg.result["type"], dlg.result["level"], dlg.result["topic_id"]))
            conn.commit()
            conn.close()
            self.load_data()

    def edit_exercise(self):
        sel = self.tree.selection()
        if not sel:
            return
        ex_id = sel[0]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM exercise WHERE exercise_id=?", (ex_id,))
        r = cur.fetchone()
        conn.close()
        dlg = AddEditExercise(self.win, data=r)
        self.win.wait_window(dlg.top)
        if dlg.result:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE exercise SET problem=?, type=?, exercise_level=?, topic_id=? WHERE exercise_id=?",
                        (dlg.result["problem"], dlg.result["type"], dlg.result["level"], dlg.result["topic_id"], ex_id))
            conn.commit()
            conn.close()
            self.load_data()

    def delete_exercise(self):
        sel = self.tree.selection()
        if not sel:
            return
        ex_id = sel[0]
        if not messagebox.askyesno("Confirm", "Delete selected exercise?"):
            return
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM exercise WHERE exercise_id=?", (ex_id,))
        conn.commit()
        conn.close()
        self.load_data()

class AddEditExercise:
    def __init__(self, parent, data=None):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title("Add / Edit Exercise")
        tk.Label(self.top, text="Problem").grid(row=0, column=0)
        self.e_problem = tk.Entry(self.top); self.e_problem.grid(row=0, column=1)
        tk.Label(self.top, text="Type").grid(row=1, column=0)
        self.e_type = tk.Entry(self.top); self.e_type.grid(row=1, column=1)
        tk.Label(self.top, text="Level").grid(row=2, column=0)
        self.e_level = tk.Entry(self.top); self.e_level.grid(row=2, column=1)
        tk.Label(self.top, text="Topic ID").grid(row=3, column=0)
        self.e_topic = tk.Entry(self.top); self.e_topic.grid(row=3, column=1)

        tk.Button(self.top, text="Save", command=self.on_save).grid(row=4, column=0, columnspan=2)

        if data:
            self.e_problem.insert(0, data["problem"])
            self.e_type.insert(0, data["type"])
            self.e_level.insert(0, data["exercise_level"])
            self.e_topic.insert(0, data["topic_id"])

    def on_save(self):
        self.result = {
            "problem": self.e_problem.get().strip(),
            "type": self.e_type.get().strip(),
            "level": self.e_level.get().strip(),
            "topic_id": self.e_topic.get().strip()
        }
        self.top.destroy()
