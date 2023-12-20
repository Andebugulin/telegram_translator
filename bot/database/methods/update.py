import sqlite3
import datetime
import json
import random


# Function to add a new user if they don't exist
def add_new_user(user_id, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id FROM user_history WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()
    
    if not existing_user:
        cursor.execute("INSERT INTO user_history (user_id, history, recalling_dates) VALUES (?, ?, ?)", (user_id, json.dumps([]), json.dumps({})))
        conn.commit()
    
    conn.close()

def check_and_add_word(word, user_id, db_name):
    conn = sqlite3.connect(db_name)
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


def remember_word(word, user_id, db_name):
    conn = sqlite3.connect(db_name)
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
    
    recalling_dates[word_id] = generate_times()
    cursor.execute("UPDATE user_history SET recalling_dates=? WHERE user_id=?", (json.dumps(recalling_dates), user_id))
    
    conn.commit()
    conn.close()

def generate_times() -> list:
    # Define a function to generate random time between 1.5 to 3 hours
    def generate_random_time():
        random_hours = random.uniform(1.5, 3)
        return datetime.timedelta(hours=random_hours)

    def decide_times(current_time, times_to_be_generated):
        updated_time = current_time

        # Initialize an empty list to store valid datetimes
        valid_datetimes = []
        while datetime.time(4, 0) < updated_time.time() < datetime.time(23, 59):
            random_time = generate_random_time()
            updated_time = updated_time + random_time
            if datetime.time(4, 0) < updated_time.time() < datetime.time(23, 59):
                valid_datetimes.append(updated_time)  # Store datetime objects

        # Trim the list to the required number of times
        while len(valid_datetimes) > times_to_be_generated:
            valid_datetimes.pop(random.randint(0, len(valid_datetimes) - 1))

        return valid_datetimes if len(valid_datetimes) > 0 else decide_times(current_time.replace(hour=7, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1), times_to_be_generated)

    # Your code for obtaining times for different days remains unchanged

    # Usage example:
    current_time = datetime.datetime.now()
    tomorrow = decide_times(current_time.replace(hour=7, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1), 3)
    next_day_after_tomorrow = decide_times(current_time.replace(hour=7, minute=0, second=0, microsecond=0) + datetime.timedelta(days=2), 2)
    two_days_after_tomorrow = decide_times(current_time.replace(hour=7, minute=0, second=0, microsecond=0) + datetime.timedelta(days=3), 1)
    three_days_after_tomorrow = decide_times(current_time.replace(hour=7, minute=0, second=0, microsecond=0) + datetime.timedelta(days=4), 1)
    four_days_after_tomorrow = decide_times(current_time.replace(hour=7, minute=0, second=0, microsecond=0) + datetime.timedelta(days=5), 1)

    times = decide_times(current_time, 4)
    times = times + tomorrow
    times = times + next_day_after_tomorrow
    times = times + two_days_after_tomorrow
    times = times + three_days_after_tomorrow
    times = times + four_days_after_tomorrow
    return times






