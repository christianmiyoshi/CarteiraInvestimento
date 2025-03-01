from datetime import date, timedelta, datetime
from functools import lru_cache

from domain.tax_calculator import TaxCalculator


IOF_PERCENT = {
    0: 100,
    1: 96,	
    2: 93,	
    3: 90,
    4: 86,	
    5: 83,	
    6: 80,
    7: 76,	
    8: 73,	
    9: 70,
    10: 66,	
    11: 63,	
    12: 60,
    13: 56,	
    14: 53,	
    15: 50,
    16: 46,	
    17: 43,	
    18: 40,
    19: 36,	
    20: 33,	
    21: 30,
    22: 26,	
    23: 23,	
    24: 20,
    25: 16,	
    26: 13,	
    27: 10,
    28: 6,	
    29: 3,	
    30: 0,
}

class RendaFixa:
    def __init__(self, value, interest_year, timestamp: datetime, maturity: datetime, tax_algorithm: TaxCalculator):
        assert timestamp < maturity
        self.interest_year = interest_year
        self.value = value
        self.timestamp = timestamp
        self.tax_algorithm = tax_algorithm

    def net_value(self, date: date):
        return self.gross_value(date) - self.tax_iof_value(date)

    def tax_iof_value(self, date: date):
        return self.tax_algorithm.calculate(self, date) + self.iof_value(date)

    def gross_income_return_after_ios(self, date: date):
        return self.gross_income_return(date) - self.iof_value(date)
    
    def gross_income_return(self, date: date):
        return self.gross_value(date) - self.value

    def iof_value(self, date: date):
        assert date >= self.timestamp.date()
        number_days = (date - self.timestamp.date()).days
        if number_days > 30:
            iof_percent = 0
            iof_tax = 0
        else:
            iof_percent = IOF_PERCENT[number_days]
            iof_tax = self.gross_income_return(date) * iof_percent / 100
        
        return iof_tax

    @lru_cache(maxsize=64)
    def gross_value(self, timestamp: date):
        number_days = RendaFixa.count_business_days(
            self.timestamp.date() + timedelta(days=1),
            timestamp
        )

        # TODO: interest rate might change depending on the year
        daily_interest_percent = RendaFixa.daily_interest_percent(
            self.interest_year,
            datetime(self.timestamp.year, 1, 1).date(),
            datetime(self.timestamp.year + 1, 1, 1).date(),
        )

        return self.value * pow((1 + daily_interest_percent), number_days)

    @staticmethod
    def count_business_days(start_included: date, end_included: date):            
        return sum(1 for idx in range((end_included - start_included).days + 1) 
                   if (start_included + timedelta(days=idx)).weekday() < 5)

    @staticmethod
    def daily_interest_percent(interest: float, start: date, end: date):
        days = RendaFixa.count_business_days(start + timedelta(days=1), end)
        return pow((1 + interest), 1/days) - 1




