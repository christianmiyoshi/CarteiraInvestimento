from datetime import date, timedelta

def is_business_day(date: date):
    return date.weekday() < 5

def count_business_days(start_included: date, end_included: date):            
    return sum(1 for idx in range((end_included - start_included).days + 1) 
                if is_business_day(start_included + timedelta(days=idx)))

def daily_interest_percent(interest: float, start: date, end: date):
    days = count_business_days(start + timedelta(days=1), end)
    return pow((1 + interest), 1/days) - 1

