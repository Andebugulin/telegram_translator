import sqlite3
import datetime
import json


def check_history_expiration(user_id, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT history FROM user_history WHERE user_id=?", (user_id,))
    history = cursor.fetchone()

    if history:
        for key, values in history.iteritems():
            if values['date']:
                # Convert the date string to a datetime object
                date = datetime.datetime.strptime(values['date'], '%Y-%m-%d')
                
                # Calculate the difference between today and the saved date
                now = datetime.datetime.now()
                difference = now - date

                # Check if it has been 15 days since the word was last reviewed
                if difference.days >= 15:
                    # Delete the word from the history
                    del history[key]

                else:
                    break

    cursor.execute("UPDATE user_history SET history=? WHERE user_id=?", (json.dumps(history), user_id))
    conn.commit()
    conn.close()
    


def delete_word_from_history(user_id, word_id, to_language, from_language, db_name): # TODO: add to_language and from_language
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT history FROM user_history WHERE user_id=?", (user_id,))
    history = cursor.fetchone()
    
    if history:
        history = json.loads(history[0])
        if word_id in history.keys():
            del history[word_id]        
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