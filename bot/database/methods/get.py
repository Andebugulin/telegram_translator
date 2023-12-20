import sqlite3
import json


def retrieve_user_history(user_id):
    conn = sqlite3.connect('translator.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT history FROM user_history WHERE user_id=?", (user_id,))
    history = cursor.fetchone()
    
    conn.close()
    
    if history:
        return json.loads(history[0])
    else:
        return []