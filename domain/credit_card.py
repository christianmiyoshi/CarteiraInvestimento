from functools import reduce

from matplotlib.dates import relativedelta
from domain.credit_card_debt import CreditCardDebt
from domain.deposit import Deposit
from domain.payment import Payment
from domain.payment_installment import PaymentInstallment
from datetime import date, datetime, timedelta


class CreditCard:
    def __init__(self, payment_day: int):
        assert payment_day <= 28

        self.payment_day = payment_day
        self.installments: list[PaymentInstallment] = []
        self.payments: list[Payment] = []

    def add_payment_installment(self, installment: PaymentInstallment):
        self.installments.append(installment)

    def deposits(self):
        deposits = []
        for installment in self.installments:
            debts = installment.debts
            card_deposits = [
                Deposit(
                    -debt.value, 
                    datetime.combine(self.next_payment_date_after_date(debt.date), datetime.min.time())
                ) 
                for debt in debts
            ]
            deposits += card_deposits

        return deposits

    def pay(self, value: float, date: date):
        self.payments.append(Payment(value, date))

    # Deprecated
    def total_debt(self, date: date):        
        list_deposits = filter(
            lambda debt: debt.timestamp.date() <= date,
            self.deposits()
        )

        sum_debt = reduce(
            lambda acc, debt: acc + -debt.value,
            list_deposits, 0
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
    
    def next_payment_date_after_date(self, date: date):
        if date.day > self.payment_day:
            last_payment_date = date.replace(day=1) + timedelta(month=1)
            last_payment_date = last_payment_date.replace(day=self.payment_day)
            return last_payment_date

        last_payment_date = date.replace(day=15)
        return last_payment_date

    def result(self, date: date):
        last_payment_date = self.last_payment_date_before_date(date)
        return self.total_payment(date) - self.total_debt(last_payment_date)

