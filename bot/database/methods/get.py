import sqlite3
import json


def retrieve_user_history(user_id, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT history FROM user_history WHERE user_id=?", (user_id,))
    history = cursor.fetchone()
    
    conn.close()
    
    if history:
        return json.loads(history[0])
    else:
        return []
    
def get_to_language(user_id, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT to_language FROM user_history WHERE user_id=?", (user_id,))
    to_language = cursor.fetchone()

    conn.close()
    
    if to_language:
        return to_language[0]
    else:
        return None

def get_from_language(user_id, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT from_language FROM user_history WHERE user_id=?", (user_id,))
    from_language = cursor.fetchone()

    conn.close()
    
    if from_language:
        return from_language[0]
    else:
        return None
    