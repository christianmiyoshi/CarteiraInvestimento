import unittest
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from domain.tax_regressive_table_calculator import TaxRegressiveTableCalculator
from services.renda_fixa_factory import RendaFixaFactory

class TestRendaFixaWithTax(unittest.TestCase):
    def setUp(self):        
        self.renda_fixa_factory = RendaFixaFactory()
        return super().setUp()
    
    def test_initial_value(self):
        start_date = datetime(2025, 1, 1, 0, 0, 0, 0)
        interest = 10.0
        maturity = start_date.date() + relativedelta(years=2)
        renda_fixa = self.renda_fixa_factory.cdb(1000,interest,start_date, maturity)
    
        self.assertEqual(renda_fixa.net_value(start_date.date()), 1000)
        self.assertEqual(renda_fixa.tax_iof_value(start_date.date()), 0)
        self.assertEqual(renda_fixa.gross_value(start_date.date()), 1000)

    def test_net_return(self):
        start_date = datetime(2025, 1, 1)
        maturity = date(2027, 1, 1)
        start_value = 1000
        interest = 0.10
        renda_fixa = self.renda_fixa_factory.cdb(start_value,interest,start_date, maturity)

        # TODO: this should be equal
        self.assertAlmostEqual(
            start_value * (1 + interest),
            renda_fixa.gross_value(
                date(2026, 1, 1)
            )
        )
        self.assertAlmostEqual(
            (start_value * (1 + interest) ** 1 - start_value ) * 0.175,
            renda_fixa.tax_iof_value(
                date(2026, 1, 1)
            ),
            10
        )
        self.assertAlmostEqual(
            (start_value * (1 + interest) ** 2 - start_value ) * 0.15,
            renda_fixa.tax_iof_value(
                date(2027, 1, 1)
            ),
            10
        )
        
if __name__ == '__main__':
    unittest.main()