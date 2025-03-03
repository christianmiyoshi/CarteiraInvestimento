from datetime import date
from domain.ir_regressive_table import (
    ir_regressive_table, calculate_calendar_days
)    
from domain.renda_fixa import RendaFixa
from domain.tax_calculator import TaxCalculator

class TaxRegressiveTableCalculator(TaxCalculator):

    def aliquota(self, calendar_days: int):
        return ir_regressive_table(calendar_days)

    def calculate(self, renda_fixa: RendaFixa, date: date):
        assert date >= renda_fixa.timestamp.date()
        income_after_iof = renda_fixa.gross_income_return_after_ios(date)
                
        calendar_days = calculate_calendar_days(
            renda_fixa.timestamp.date(), date
        )
        percent = ir_regressive_table(calendar_days)

        return income_after_iof * percent
