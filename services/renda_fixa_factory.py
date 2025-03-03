from datetime import datetime

from domain.index import Indice, NoIndice
from domain.renda_fixa import RendaFixa
from domain.renda_fixa_daily_liquidity import RendaFixaDailyLiquidity
from domain.tax_free_calculator import TaxFreeCalculator
from domain.tax_regressive_table_calculator import TaxRegressiveTableCalculator

NO_INDEX = NoIndice()

class RendaFixaFactory:
    def lci(self, value, interest_year, timestamp: datetime, maturity: datetime):
        return RendaFixa(
            value, interest_year, timestamp, maturity,
            TaxFreeCalculator(),
            NO_INDEX
        )
    
    def lci_floating_rate(self, value, interest_year, timestamp: datetime, maturity: datetime, indice: Indice):
        return RendaFixa(
            value, interest_year, timestamp, maturity,
            TaxFreeCalculator(),
            indice
        )
    
    def cdb(self, value, interest_year, timestamp: datetime, maturity: datetime):
        return RendaFixa(
            value, interest_year, timestamp, maturity,
            TaxRegressiveTableCalculator(),
            NO_INDEX
        )

    def cdb_liquidity(self, value, interest_year, timestamp: datetime, maturity: datetime):
        return RendaFixaDailyLiquidity(
            value, interest_year, timestamp, maturity,
            TaxRegressiveTableCalculator(),
            NO_INDEX
        )