from functools import reduce

from matplotlib.dates import relativedelta
from domain.credit_card_debt import CreditCardDebt
from domain.payment import Payment
from domain.payment_installment import PaymentInstallment
from datetime import date, timedelta


class CreditCard:
    def __init__(self, payment_day: int):
        assert payment_day <= 28

        self.payment_day = payment_day
        self.installments: list[PaymentInstallment] = []
        self.debts: list[CreditCardDebt] = []

        self.payments: list[Payment] = []

    def add_payment_installment(self, installment: PaymentInstallment):
        self.installments.append(installment)
        self.debts += installment.payments

    def pay(self, value: float, date: date):
        self.payments.append(Payment(value, date))

    def total_debt(self, date: date):
        list_debts = filter(
            lambda debt: debt.date <= date,
            self.debts
        )

        sum_debt = reduce(
            lambda acc, debt: acc + debt.debt(),
            list_debts, 0
        )
        return sum_debt

    def total_payment(self, date: date):
        list_payments = filter(
            lambda payment: payment.date <= date,
            self.payments
        )

        sum_payments = reduce(
            lambda acc, payment: acc + payment.value,
            list_payments, 0
        )
        return sum_payments
    
    def last_payment_date_before_date(self, date: date):
        if date.day < self.payment_day:
            last_payment_date = date.replace(day=1) - timedelta(days=1)
            last_payment_date = last_payment_date.replace(day=self.payment_day)
            return last_payment_date

        last_payment_date = date.replace(day=15)
        return last_payment_date

    def result(self, date: date):
        last_payment_date = self.last_payment_date_before_date(date)
        return self.total_payment(date) - self.total_debt(last_payment_date)

