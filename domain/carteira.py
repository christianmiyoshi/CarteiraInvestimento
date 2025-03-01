import datetime
from functools import reduce
from domain.renda_fixa import RendaFixa
from domain.deposit import Deposit


class Wallet:
    def __init__(self):
        self.deposits: list[Deposit] = []

    def deposit(self, value: float, timestamp: datetime.datetime):
        self.deposits.append(
            Deposit(value, timestamp)
        )

    def withdraw(self, value: float, timestamp: datetime.datetime):
        self.deposits.append(
            Deposit(-value, timestamp)
        )

    def net_value(self, date: datetime.date):
        return self.brut_value(date) - self.tax_value(date)

    def tax_value(self, date: datetime.date):
        return 0

    def brut_value(self, timestamp: datetime.datetime):
        sum_deposits = reduce(
            lambda acc, deposit: acc + deposit.value_at(timestamp),
            self.deposits, 0
        )
        return sum_deposits
