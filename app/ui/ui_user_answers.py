import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from app.db import get_connection

class UserExerciseWindow:
    def __init__(self, user: dict):
        self.user = user
        self.win = tk.Toplevel()
        self.win.title("User Answers")
        self.win.geometry("900x480")

        cols = ("user_answer_id","user_id","user_name","exercise_id","answer_text","part_number","is_complete","created_at")
        self.tree = ttk.Treeview(self.win, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)
        self.tree.pack(fill="both", expand=True)

        frame = tk.Frame(self.win); frame.pack(fill="x", pady=6)
        tk.Button(frame, text="Add Answer", command=self.add_answer).pack(side="left", padx=5)
        tk.Button(frame, text="Edit Answer", command=self.edit_answer).pack(side="left", padx=5)
        tk.Button(frame, text="Mark Complete/Uncomplete", command=self.toggle_complete).pack(side="left", padx=5)
        tk.Button(frame, text="Refresh", command=self.load_data).pack(side="left", padx=5)
        if self.user["role"] in ("admin","teacher"):
            tk.Button(frame, text="Delete Answer", command=self.delete_answer).pack(side="left", padx=5)

        self.load_data()

    def load_data(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        conn = get_connection(); cur = conn.cursor()
        if self.user["role"] in ("admin","teacher"):
            cur.execute("""
                SELECT ua.user_answer_id, ua.user_id, u.name as user_name, ua.exercise_id, ua.answer_text, ua.part_number, ua.is_complete, ua.created_at
                FROM user_exercise_answer ua
                LEFT JOIN users u ON u.user_id = ua.user_id
                ORDER BY ua.created_at DESC
            """)
            rows = cur.fetchall()
        else:
            cur.execute("""
                SELECT ua.user_answer_id, ua.user_id, u.name as user_name, ua.exercise_id, ua.answer_text, ua.part_number, ua.is_complete, ua.created_at
                FROM user_exercise_answer ua
                LEFT JOIN users u ON u.user_id = ua.user_id
                WHERE ua.user_id = ?
                ORDER BY ua.created_at DESC
            """, (self.user["user_id"],))
            rows = cur.fetchall()
        for row in rows:
            self.tree.insert("", "end", iid=row["user_answer_id"], values=(
                row["user_answer_id"], row["user_id"], row["user_name"], row["exercise_id"], row["answer_text"], row["part_number"], row["is_complete"], row["created_at"]
            ))
        conn.close()

    def add_answer(self):
        # both student and admin/teacher can add (admin will create on behalf)
        ex_id = simpledialog.askinteger("Exercise ID", "Enter Exercise ID:", parent=self.win)
        if ex_id is None: return
        ans = simpledialog.askstring("Answer", "Enter your answer:", parent=self.win)
        if ans is None: return
        # user_id is current user for students; admin can add for themselves as well
        user_id = self.user["user_id"]
        conn = get_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO user_exercise_answer (user_id, exercise_id, answer_text) VALUES (?,?,?)", (user_id, ex_id, ans))
        conn.commit(); conn.close()
        self.load_data()

    def edit_answer(self):
        sel = self.tree.selection()
        if not sel: return
        aid = sel[0]
        # permission: student can only edit their own
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT user_id, answer_text FROM user_exercise_answer WHERE user_answer_id=?", (aid,))
        row = cur.fetchone()
        conn.close()
        if not row: return
        if self.user["role"] == "student" and row["user_id"] != self.user["user_id"]:
            messagebox.showerror("Error", "You can't edit others' answers")
            return
        new_text = simpledialog.askstring("Edit Answer", "Update your answer:", initialvalue=row["answer_text"], parent=self.win)
        if new_text is None: return
        conn = get_connection(); cur = conn.cursor()
        cur.execute("UPDATE user_exercise_answer SET answer_text=? WHERE user_answer_id=?", (new_text, aid))
        conn.commit(); conn.close()
        self.load_data()

    def toggle_complete(self):
        sel = self.tree.selection()
        if not sel: return
        aid = sel[0]
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT is_complete FROM user_exercise_answer WHERE user_answer_id=?", (aid,))
        r = cur.fetchone()
        if not r: conn.close(); return
        new = 0 if r["is_complete"] else 1
        cur.execute("UPDATE user_exercise_answer SET is_complete=? WHERE user_answer_id=?", (new, aid))
        conn.commit(); conn.close()
        self.load_data()

    def delete_answer(self):
        if self.user["role"] not in ("admin","teacher"): return
        sel = self.tree.selection()
        if not sel: return
        aid = sel[0]
        if not messagebox.askyesno("Confirm", "Delete selected answer?"): return
        conn = get_connection(); cur = conn.cursor()
        cur.execute("DELETE FROM user_exercise_answer WHERE user_answer_id=?", (aid,))
        conn.commit(); conn.close()
        self.load_data()
