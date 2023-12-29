import sqlite3
import json

def initialize_database(db_name):
    # history is a dictionary 
    # with keys          as word_ids 
    # and
    # values             as translations, from what language, to what language, and when translated

    # recalling_dates is a dictionary
    # with keys          as word_ids
    # and
    # values             as dates for the word to be recalled.
    conn = sqlite3.connect(db_name)
    conn.execute('''CREATE TABLE IF NOT EXISTS user_history (
                    user_id INTEGER,
                    history TEXT,
                    recalling_dates TEXT,
                    from_language TEXT, 
                    to_language TEXT,  
                    FOREIGN KEY (user_id) REFERENCES users(id)
                    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS dictionary (
                    word_id INTEGER PRIMARY KEY
                    )''')
    
    conn.commit()
    conn.close()#



