from datetime import date

def ir_regressive_table(calendar_days):
    if calendar_days <= 180:
        return 0.225
    elif calendar_days <= 360:
        return 0.20
    elif calendar_days <= 720:
        return 0.175
    return 0.15

def calculate_calendar_days(start: date, end: date):
    return (end - start).days