import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from app.db import get_connection

class UsersWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Users")
        self.win.geometry("700x400")

        self.tree = ttk.Treeview(self.win, columns=("name","email","role"), show="headings")
        for col, title in [("name","Name"), ("email","Email"), ("role","Role")]:
            self.tree.heading(col, text=title)
            self.tree.column(col, width=200)
        self.tree.pack(fill="both", expand=True)

        frame = tk.Frame(self.win)
        frame.pack(fill="x", pady=6)
        tk.Button(frame, text="Add", command=self.add_user).pack(side="left", padx=5)
        tk.Button(frame, text="Edit", command=self.edit_user).pack(side="left", padx=5)
        tk.Button(frame, text="Delete", command=self.delete_user).pack(side="left", padx=5)
        tk.Button(frame, text="Refresh", command=self.load_data).pack(side="left", padx=5)

        self.load_data()

    def load_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, name, email, role FROM users")
        for row in cur.fetchall():
            self.tree.insert("", "end", iid=row["user_id"], values=(row["name"], row["email"], row["role"]))
        conn.close()

    def add_user(self):
        dlg = AddEditUser(self.win)
        self.win.wait_window(dlg.top)
        if dlg.result:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name,email,role) VALUES (?, ?, ?)",
                        (dlg.result["name"], dlg.result["email"], dlg.result["role"]))
            conn.commit()
            conn.close()
            self.load_data()

    def edit_user(self):
        sel = self.tree.selection()
        if not sel:
            return
        user_id = sel[0]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        r = cur.fetchone()
        conn.close()
        dlg = AddEditUser(self.win, data=r)
        self.win.wait_window(dlg.top)
        if dlg.result:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET name=?, email=?, role=? WHERE user_id=?",
                        (dlg.result["name"], dlg.result["email"], dlg.result["role"], user_id))
            conn.commit()
            conn.close()
            self.load_data()

    def delete_user(self):
        sel = self.tree.selection()
        if not sel:
            return
        user_id = sel[0]
        if not messagebox.askyesno("Confirm", "Delete selected user?"):
            return
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        conn.commit()
        conn.close()
        self.load_data()

class AddEditUser:
    def __init__(self, parent, data=None):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title("Add / Edit User")
        tk.Label(self.top, text="Name").grid(row=0, column=0)
        self.e_name = tk.Entry(self.top); self.e_name.grid(row=0, column=1)
        tk.Label(self.top, text="Email").grid(row=1, column=0)
        self.e_email = tk.Entry(self.top); self.e_email.grid(row=1, column=1)
        tk.Label(self.top, text="Role").grid(row=2, column=0)
        self.e_role = tk.Entry(self.top); self.e_role.grid(row=2, column=1)

        tk.Button(self.top, text="Save", command=self.on_save).grid(row=3, column=0, columnspan=2)

        if data:
            self.e_name.insert(0, data["name"])
            self.e_email.insert(0, data["email"])
            self.e_role.insert(0, data["role"])

    def on_save(self):
        self.result = {
            "name": self.e_name.get().strip(),
            "email": self.e_email.get().strip(),
            "role": self.e_role.get().strip()
        }
        self.top.destroy()
