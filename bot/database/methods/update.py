import sqlite3
from datetime import datetime
import json
import random


# Function to add a new user if they don't exist
def add_new_user(user_id):
    conn = sqlite3.connect('translator.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id FROM user_history WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()
    
    if not existing_user:
        cursor.execute("INSERT INTO user_history (user_id, history, recalling_dates) VALUES (?, ?, ?)", (user_id, json.dumps([]), json.dumps({})))
        conn.commit()
    
    conn.close()

def check_and_add_word(word, user_id):
    conn = sqlite3.connect('translator.db')
    cursor = conn.cursor()
    
    # Check if the word is in the dictionary
    cursor.execute("SELECT word_id FROM dictionary WHERE word_id=?", (word,))
    word_id = cursor.fetchone()
    
    # If the word doesn't exist, add it to the dictionary
    if not word_id:
        cursor.execute("INSERT INTO dictionary (word_id) VALUES (?)", (word,))
        conn.commit()
        word_id = cursor.lastrowid
    
    # Add the word to user history
    user_id = user_id  
    cursor.execute("SELECT history FROM user_history WHERE user_id=?", (user_id,))
    history = cursor.fetchone()
    
    if history:
        history = json.loads(history[0])
        history.append(word_id)
        cursor.execute("UPDATE user_history SET history=? WHERE user_id=?", (json.dumps(history), user_id))
    else:
        cursor.execute("INSERT INTO user_history (user_id, history) VALUES (?, ?)", (user_id, json.dumps([word_id])))
    
    conn.commit()
    conn.close()


def remember_word(word, user_id):
    conn = sqlite3.connect('translator.db')
    cursor = conn.cursor()

    # Check if the word is in the dictionary
    cursor.execute("SELECT word_id FROM dictionary WHERE word_id=?", (word,))
    word_id = cursor.fetchone()

    if not word_id:
        conn.commit()
        conn.close()
        return
    
    cursor.execute("SELECT recalling_dates FROM user_history WHERE user_id=?", (user_id,))
    recalling_dates = cursor.fetchone()
    recalling_dates = json.loads(recalling_dates[0]) if recalling_dates else {}
    
    recalling_dates[word_id] = []

    # TODO: append needed dates
    recalling_dates[word_id].append(datetime.now().strftime("%Y-%m-%d"))
    cursor.execute("UPDATE user_history SET recalling_dates=? WHERE user_id=?", (json.dumps(recalling_dates), user_id))
    
    conn.commit()
    conn.close()






