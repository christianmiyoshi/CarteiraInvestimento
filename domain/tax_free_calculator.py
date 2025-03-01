from datetime import date
from domain.renda_fixa import RendaFixa
from domain.tax_calculator import TaxCalculator

class TaxFreeCalculator(TaxCalculator):
    def calculate(self, renda_fixa: RendaFixa, date: date):
        return 0

        
