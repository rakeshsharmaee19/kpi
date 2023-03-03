import datetime
from datetime import datetime, timedelta


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def week_sprint(project_id, start_date, end_date, feedback_frequency):
    if feedback_frequency == "Week":
        feedback_frequency = 7
    else:
        feedback_frequency = 15
    result = []
    days = abs(start_date - end_date).days
    num_of_div = days // feedback_frequency
    temp = start_date
    i = 1
    while i <= num_of_div:
        enddate = temp + timedelta(days=feedback_frequency)
        if (enddate - end_date).days > 0:
            result.append({"project_id":project_id, "sprint_number": i, "start_date": temp.strftime("%Y-%m-%d"), "end_date": end_date.strftime("%Y-%m-%d")})
        else:
            result.append({"project_id":project_id, "sprint_number": i, "start_date": temp.strftime("%Y-%m-%d"), "end_date": enddate.strftime("%Y-%m-%d")})
        temp = temp + timedelta(days=feedback_frequency + 1)
        i = i + 1
        if (temp - end_date).days > 0:
            break
    return result


def datedivide(project_id, begin, end, feedback_frequency):
    if feedback_frequency == "Month":
        result = []
        i = 0
        while True:
            i = i + 1
            if begin.month == 12:
                next_month = begin.replace(year=begin.year + 1, month=1, day=1)
            else:
                next_month = begin.replace(month=begin.month + 1, day=1)
            if next_month > end:
                break
            result.append({"project_id": project_id, "sprint_number": i, "start_date": begin.strftime("%Y-%m-%d"), "end_date": last_day_of_month(begin).strftime("%Y-%m-%d")})
            begin = next_month
        result.append({"project_id": project_id, "sprint_number": i, "start_date":begin.strftime("%Y-%m-%d"), "end_date": end.strftime("%Y-%m-%d")})

        return result
    elif feedback_frequency == "Week" or feedback_frequency == "Sprint":
        return week_sprint(project_id, begin, end, feedback_frequency)

