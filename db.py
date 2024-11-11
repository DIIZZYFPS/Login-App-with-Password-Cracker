import sqlite3
import hashlib

class UserDatabase:
    def __init__(self, db_name='users.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL)''')
        self.connection.commit()

    def add_user(self, username, password):
        hashword = self.hash_password(password)
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashword))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def hash_password(self, password):
        return hashlib.sha512(password.encode()).hexdigest()

    def validate_user(self, username, password):
        hashword = self.hash_password(password)
        self.cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hashword))
        return self.cursor.fetchone() is not None

    def close(self):
        self.connection.close()