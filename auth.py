import hashlib
import sqlite3
from database import get_db_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class AuthManager:
    @staticmethod
    def register(username, password, role="student"):
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           (username, hashed_password, role))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Foydalanuvchi allaqachon mavjud!")
        conn.close()

    @staticmethod
    def login(username, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                       (username, hashed_password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return user
        return None
