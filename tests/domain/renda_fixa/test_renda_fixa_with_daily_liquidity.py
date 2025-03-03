import unittest
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from domain.tax_regressive_table_calculator import TaxRegressiveTableCalculator
from services.renda_fixa_factory import RendaFixaFactory

class TestRendaFixaWithDailyLiquidity(unittest.TestCase):
    def setUp(self):        
        self.renda_fixa_factory = RendaFixaFactory()
        return super().setUp()

    def test_gross_return(self):
        # An investment of 1000 = investment of 92.37875289 and 907.6212471
        # After one year with 10% of interest and tax of 20%,
        # the investment of 92.37875289 will value 101.6166281755, 100.00 is net value and 1.616628176 is tax
        # Therefore, after withdrawing 100, all the investment of 92.37875289 has been withdrawn
        # The investment of 907.6212471 will become 1199.8383371825 after two years
        # The gross value of the investment after two years will be 1199.8383371825 + 101.6166281755 = 1199.8383371825

        start_date = datetime(2025, 1, 1)
        maturity = date(2027, 1, 1)
        start_value = 1000
        interest = 0.10
        renda_fixa = self.renda_fixa_factory.cdb_liquidity(start_value,interest,start_date, maturity)

        renda_fixa.withdraw(100, date(2026, 1, 1))

        self.assertAlmostEqual(
            1100,
            renda_fixa.gross_value(
                date(2026, 1, 1)
            ),
            10
        )
        self.assertAlmostEqual(
            1199.8383371825,
            renda_fixa.gross_value(
                date(2027, 1, 1)
            ),
            9
        )
        
if __name__ == '__main__':
    unittest.main()