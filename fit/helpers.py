# Function for calendar index (placement)
def cal_index(day, time):
    # Define a number for each day of the week for calculation
    match day:
        case "Monday":
            day = 0
        case "Tuesday":
            day = 10
        case "Wednesday":
            day = 20
        case "Thursday":
            day = 30
        case "Friday":
            day = 40
        case "Saturday":
            day = 50
        case "Sunday":
            day = 60
    # Define a number for each time for calculation
    match time[:2]:
        case "00":
            time = 0
        case "06":
            time = 1
        case "08":
            time = 2
        case "10":
            time = 3
        case "12":
            time = 4
        case "14":
            time = 5
        case "16":
            time = 6
        case "18":
            time = 7
        case "20":
            time = 8
        case "22":
            time = 9

    return time + day
 
