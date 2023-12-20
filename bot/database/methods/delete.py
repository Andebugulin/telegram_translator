import sqlite3
import json


def delete_word_from_history(user_id, word_id, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT history FROM user_history WHERE user_id=?", (user_id,))
    history = cursor.fetchone()
    
    if history:
        history = json.loads(history[0])
        if word_id in history:
            history.remove(word_id)
            cursor.execute("UPDATE user_history SET history=? WHERE user_id=?", (json.dumps(history), user_id))
    
    # Remove the word from recalling dates
    cursor.execute("SELECT recalling_dates FROM user_history WHERE user_id=?", (user_id,))
    recalling_dates = cursor.fetchone()
    
    if recalling_dates:
        recalling_dates = json.loads(recalling_dates[0])
        if word_id in recalling_dates:
            del recalling_dates[word_id]
    cursor.execute("UPDATE user_history SET recalling_dates=? WHERE user_id=?", (json.dumps(recalling_dates), user_id))
    
    conn.commit()
    conn.close()

def delete_user(user_id, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Delete the user's history from the user_history table
    cursor.execute("DELETE FROM user_history WHERE user_id = ?", (user_id,))
    
    conn.commit()
    conn.close()