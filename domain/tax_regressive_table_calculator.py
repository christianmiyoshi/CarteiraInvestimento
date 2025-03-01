from datetime import date
from domain.renda_fixa import RendaFixa
from domain.tax_calculator import TaxCalculator

class TaxRegressiveTableCalculator(TaxCalculator):
    def calculate(self, renda_fixa: RendaFixa, date: date):
        assert date >= renda_fixa.timestamp.date()
        income_after_iof = renda_fixa.gross_income_return_after_ios(date)

        calendar_days = (date - renda_fixa.timestamp.date()).days

        if calendar_days <= 180:
            percent = 0.225
        elif calendar_days <= 360:
            percent = 0.20
        elif calendar_days <= 720:
            percent = 0.175
        else:
            percent = 0.15

        return income_after_iof * percent
