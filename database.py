
import sqlite3
from flask_login import UserMixin

DB_NAME = 'users.db'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.close()

def create_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None
