from datetime import date, timedelta, datetime
from functools import lru_cache

from domain.helper.interest_helper import count_business_days, daily_interest_percent
from domain.index import Indice
from domain.ir_regressive_table import ir_regressive_table, calculate_calendar_days
from domain.deposit import Deposit
from domain.iof_constant import IOF_PERCENT
from domain.tax_calculator import TaxCalculator

class RendaFixa:
    def __init__(self, value, interest_year, timestamp: datetime, maturity: date, tax_algorithm: TaxCalculator, indice: Indice):
        assert timestamp.date() < maturity
        self.interest_year = interest_year
        self.value = value
        self.maturity = maturity
        self.timestamp = timestamp
        self.tax_algorithm = tax_algorithm
        self.indice = indice

    def deposits(self):
        withdraw = Deposit(-self.value, self.timestamp)
        deposit = Deposit(self.net_value(self.maturity), datetime.combine(self.maturity, datetime.min.time()))
        return [withdraw, deposit]

    def calculate_investment_to_have_net_value(self, current_value: float, date: date):
        # Cf = C0 (1 + r) ^ t
        # K = (1 - aliqIR)
        # Rl = (Cf - C0) (1 - aliqIR) = (Cf - C0) * K
        # Lf = Rl + C0 = K Cf - K C0 + C0
        # C0 = Lf / (K (1+r)^t - K + 1)
        calendar_days = calculate_calendar_days(self.timestamp.date(), min(date, self.maturity))
        aliquota = ir_regressive_table(calendar_days)
        aliquota_sub_1 = (1 - aliquota)
        interest_percent = daily_interest_percent(
            self.interest_year,
            datetime(self.timestamp.year, 1, 1).date(),
            datetime(self.timestamp.year + 1, 1, 1).date(),
        )
        number_days = count_business_days(
            self.timestamp.date() + timedelta(days=1),
            min(date, self.maturity)
        )

        numerator = current_value        
        denominator = aliquota_sub_1 * (1 + interest_percent)**number_days - aliquota_sub_1 + 1

        return numerator / denominator

    def current_value(self, date: date):
        if date < self.timestamp:
            return 0
        if date >= self.maturity:
            return 0
        return self.net_value()

    def net_value(self, date: date):
        return self.gross_value(date) - self.tax_iof_value(date)

    def tax_iof_value(self, date: date):
        return self.tax_algorithm.calculate(self, date) + self.iof_value(date)

    def gross_income_return_after_ios(self, date: date):
        return self.gross_income_return(date) - self.iof_value(date)
    
    def gross_income_return(self, date: date):
        return self.gross_value(date) - self.value

    def iof_value(self, date: date):
        date = min(self.maturity, date)
        assert date >= self.timestamp.date()
        number_days = (date - self.timestamp.date()).days
        if number_days > 30:
            iof_percent = 0
            iof_tax = 0
        else:
            iof_percent = IOF_PERCENT[number_days]
            iof_tax = self.gross_income_return(date) * iof_percent / 100
        
        return iof_tax

    def gross_value(self, timestamp: date):
        number_days = count_business_days(
            self.timestamp.date() + timedelta(days=1),
            min(timestamp, self.maturity)
        )
        
        daily_interest_percent = self.daily_percent()
        percent_in_period = pow((1 + daily_interest_percent), number_days)
        percent_indice_in_period = self.indice.get_interest_in_period(
            self.timestamp.date(), min(timestamp, self.maturity)
        )

        return self.value * ((percent_in_period - 1) + (percent_indice_in_period - 1) + 1)

    def daily_percent(self):
        # TODO: interest rate might change depending on the year
        percent = daily_interest_percent(
            self.interest_year,
            datetime(self.timestamp.year, 1, 1).date(),
            datetime(self.timestamp.year + 1, 1, 1).date(),
        )
        
        return percent


