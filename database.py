import sqlite3

def connect_db():
    return sqlite3.connect('expenses.db')

def init_db():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS expenses(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    date TEXT,
                    category TEXT,
                    amount REAL,
                    description TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )''')

    conn.commit()
    conn.close()

def create_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users(username, password) VALUES(?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user[0] if user else None
