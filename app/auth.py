from app.db import get_connection

DEFAULT_PASSWORDS = {
    "admin": "admin123",
    "student": "student123",
    "teacher": "teacher123"
}

def authenticate(email: str, password: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, email, role FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None
    role = row['role'] # Проверяю, что там с ролью - базочка

    expected = DEFAULT_PASSWORDS.get(role)
    if expected and password == expected:
        return dict(role)
    return None