from datetime import date

class CreditCardDebt:
    def __init__(self, value: float, date: date):
        self.value = value
        self.date = date

    def pay(self):
        self.is_paid = True

    def debt(self):
        return self.value