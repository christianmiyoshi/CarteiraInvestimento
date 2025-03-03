import datetime
from datetime import date
from functools import reduce
from domain.credit_card import CreditCard
from domain.renda_fixa import RendaFixa
from domain.deposit import Deposit


class Wallet:
    def __init__(self):
        self.deposits: list[Deposit] = []
        self.credit_cards: list[CreditCard] = []

    def add_credit_card(self, credit_card: CreditCard):
        self.credit_cards.append(credit_card)

    def deposit(self, value: float, timestamp: datetime.datetime):
        self.deposits.append(Deposit(value, timestamp))

    def add_deposit(self, deposit: Deposit):
        self.deposits.append(deposit)

    def credit_card_debt(self, date: date):
        list_card_debt = map(
            lambda card: max(0, -card.result(date)),
            self.credit_cards,
        )
        return sum(list_card_debt)

    def pay_card(self, card: CreditCard, value: float, timestamp: datetime.datetime):
        assert card in self.credit_cards
        card.pay(value, timestamp.date())
        self.withdraw(value, timestamp)

    def pay_whole_debt(self, card: CreditCard, timestamp: datetime.datetime):
        assert card in self.credit_cards
        result = card.result(timestamp.date())
        if result < 0:
            self.pay_card(card, abs(result), timestamp)

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
