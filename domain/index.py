from abc import ABC, abstractmethod
from datetime import date, timedelta

from domain.helper.interest_helper import count_business_days, daily_interest_percent, is_business_day


class InterestDate:
    def __init__(self, date: date, interest_year: float):
        self.date = date
        self.interest = interest_year

class Indice(ABC):
    @abstractmethod
    def get_year_interest_at(self, date: date):
        pass

    @abstractmethod
    def get_interest_in_period(self, start: date, end:date):
        pass

class NoIndice(Indice):
    def get_year_interest_at(self, date: date):
        return 0

    def get_interest_in_period(self, start: date, end:date):
        return 1
    
class RangedIndex(Indice):
    def __init__(self, name: str):
        self.name = name
        self.interest_list: list[InterestDate] = []

    def add_intereset(self, date: date, interest: float):
        self.interest_list.append(
            InterestDate(date, interest)
        )
        self.interest_list.sort(key=lambda interest: interest.date)

    def get_year_interest_at(self, date: date):
        if not is_business_day(date):
            return 0

        filtered_items = [item for item in self.interest_list if item.date <= date]
        if not filtered_items:
            raise Exception(f'No interest for date {date}')
        return max(filtered_items, key=lambda x: x.date).interest
    
    def get_interest_in_period(self, start: date, end:date):
        # TODO: code naive. This must be improved
        number_days = count_business_days(start + timedelta(days=1), end)
        if number_days == 0:
            return 1
        
        period_interest = 1.0
        for i in range((end - start).days):
            current_date = start + timedelta(days=i)
            year_interest = self.get_year_interest_at(current_date)

            daily_percent = daily_interest_percent(
                year_interest,
                date(current_date.year, 1, 1),
                date(current_date.year + 1, 1, 1),
            )

            period_interest *= (1 + daily_percent)

        return period_interest
