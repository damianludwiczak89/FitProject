# Function for calendar index (placement)
def cal_index(day, time):
    set_day = {"Monday": 0, "Tuesday": 10, "Wednesday": 20, "Thursday": 30, "Friday": 40, "Saturday": 50, "Sunday": 60}
    set_time = {"00": 0, "06": 1, "08": 2, "10": 3, "12": 4, "14": 5, "16": 6, "18": 7, "20": 8, "22": 9}
    return set_day[day] + set_time[time[:2]]