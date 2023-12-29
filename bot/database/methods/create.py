import sqlite3
import json

def initialize_database(db_name):
    conn = sqlite3.connect(db_name)
    conn.execute('''CREATE TABLE IF NOT EXISTS user_history (
                    user_id INTEGER,
                    history TEXT,
                    recalling_dates TEXT,
                    from_language TEXT, 
                    to_language TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) -- Add foreign key constraint if users table exists
                    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS dictionary (
                    word_id INTEGER PRIMARY KEY,
                    from_language TEXT, 
                    to_language TEXT
                    )''')
    
    
    conn.commit()
    conn.close()#



