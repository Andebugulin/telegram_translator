import datetime
import random

# Define a function to generate random time between 1.5 to 3 hours
def generate_random_time():
    random_hours = random.uniform(1.5, 3)
    return datetime.timedelta(hours=random_hours)

def decide_times(current_time, times_to_be_generated):
    updated_time = current_time

    # Initialize an empty list to store valid datetimes
    valid_datetimes = []
    while datetime.time(6, 0) < updated_time.time() < datetime.time(23, 59):
        random_time = generate_random_time()
        updated_time = updated_time + random_time
        if datetime.time(6, 0) < updated_time.time() < datetime.time(23, 59):
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

# Print the valid times added to the array
print("Valid times added to the array:")
for time in times:
    print(time)
