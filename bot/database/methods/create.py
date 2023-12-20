import sqlite3
import json

def initialize_database(db_name):
    conn = sqlite3.connect(db_name)
    conn.execute('''CREATE TABLE IF NOT EXISTS user_history (
                    user_id INTEGER,
                    history TEXT,
                    recalling_dates TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS dictionary (
                    word_id INTEGER PRIMARY KEY
                    )''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
