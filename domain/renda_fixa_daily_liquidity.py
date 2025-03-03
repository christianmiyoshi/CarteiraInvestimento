from datetime import date, timedelta, datetime
from functools import lru_cache, reduce
import copy

from domain.index import Indice
from domain.iof_constant import IOF_PERCENT
from domain.renda_fixa import RendaFixa
from domain.tax_calculator import TaxCalculator

class RendaFixaDailyLiquidity(RendaFixa):
    def __init__(self, *args, **kwargs):
        self.main_renda_fixa = RendaFixa(*args, **kwargs)
        self.renda_fixas: list[RendaFixa] = [self.main_renda_fixa]

    def withdraw(self, value: float, date: date):
        assert date >= self.main_renda_fixa.timestamp.date()
        assert date <= self.main_renda_fixa.maturity

        net_value = self.main_renda_fixa.net_value(date)

        if net_value < value:
            raise Exception("There is not enoght balance to withdraw")

        self.renda_fixas.remove(self.main_renda_fixa)

        initial_investment_for_value = self.main_renda_fixa.calculate_investment_to_have_net_value(value, date)

        self.main_renda_fixa = copy.deepcopy(self.main_renda_fixa)
        self.main_renda_fixa.value -= initial_investment_for_value
        self.renda_fixas.append(self.main_renda_fixa)

        second_investment = copy.deepcopy(self.main_renda_fixa)
        second_investment.value = initial_investment_for_value
        second_investment.maturity = date
        self.renda_fixas.append(second_investment)

    def deposits(self):
        deposits_list = []
        for renda in self.renda_fixas:
            deposits_list += renda.deposits()
        return deposits_list

    def current_value(self, date: date):
        return reduce(
            lambda acc, renda: acc + renda.current_value(date),
            self.renda_fixas, 0
        )

    def net_value(self, date: date):
        return reduce(
            lambda acc, renda: acc + renda.net_value(date),
            self.renda_fixas, 0
        )

    def tax_iof_value(self, date: date):
        return reduce(
            lambda acc, renda: acc + renda.tax_iof_value(date),
            self.renda_fixas, 0
        )

    def gross_income_return_after_ios(self, date: date):
        return reduce(
            lambda acc, renda: acc + renda.gross_income_return_after_ios(date),
            self.renda_fixas, 0
        )
    
    def gross_income_return(self, date: date):
        return reduce(
            lambda acc, renda: acc + renda.gross_income_return(date),
            self.renda_fixas, 0
        )

    def iof_value(self, date: date):
        return reduce(
            lambda acc, renda: acc + renda.iof_value(date),
            self.renda_fixas, 0
        )

    def gross_value(self, timestamp: date):
        return reduce(
            lambda acc, renda: acc + renda.gross_value(timestamp),
            self.renda_fixas, 0
        )



