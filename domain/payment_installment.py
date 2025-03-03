from datetime import date

from matplotlib.dates import relativedelta

from domain.credit_card_debt import CreditCardDebt

class PaymentInstallment:

    def __init__(self, start: date, monthly_payment: float, number_installments: int):
        assert number_installments > 0
        assert monthly_payment > 0

        self.start = start
        self.monthly_payment = monthly_payment
        self.number_installments = number_installments
        self.paid_months = 0

        self.payments: list[CreditCardDebt] = []

        current_date = self.start        
        for month in range(number_installments):
            self.payments.append(
                CreditCardDebt(
                    self.monthly_payment,
                    (current_date + relativedelta(months=month)).date(),
                )
            )

    def pay(self):
        assert self.paid_months < self.number_installments
        self.paid_months += 1

    def debt(self):
        return (self.number_installments - self.paid_months) * self.monthly_payment

    def paid_value(self):
        return self.paid_months * self.monthly_payment

    @staticmethod
    def diff_months(date1: date, date2: date):
        months_diff = (date2.year - date1.year) * 12 + date2.month - date1.month
        return abs(months_diff)

    def pay_up_to_date(self, date: date):
        if date < self.start:
            self.paid_months = 0
            return 

        months = PaymentInstallment.diff_months(date, self.start) + 1
        self.paid_months = months

    