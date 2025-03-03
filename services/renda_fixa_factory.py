from datetime import datetime

from domain.renda_fixa import RendaFixa
from domain.renda_fixa_daily_liquidity import RendaFixaDailyLiquidity
from domain.tax_free_calculator import TaxFreeCalculator
from domain.tax_regressive_table_calculator import TaxRegressiveTableCalculator

class RendaFixaFactory:
    def lci(self, value, interest_year, timestamp: datetime, maturity: datetime):
        return RendaFixa(
            value, interest_year, timestamp, maturity,
            TaxFreeCalculator()
        )
    
    def cdb(self, value, interest_year, timestamp: datetime, maturity: datetime):
        return RendaFixa(
            value, interest_year, timestamp, maturity,
            TaxRegressiveTableCalculator()
        )

    def cdb_liquidity(self, value, interest_year, timestamp: datetime, maturity: datetime):
        return RendaFixaDailyLiquidity(
            value, interest_year, timestamp, maturity,
            TaxRegressiveTableCalculator()
        )