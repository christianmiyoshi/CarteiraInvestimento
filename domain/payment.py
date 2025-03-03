from datetime import date

class Payment:
    def __init__(self, value: float, date: date):
        self.value = value
        self.date = date
