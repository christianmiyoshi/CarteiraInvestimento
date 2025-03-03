import unittest
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from domain.renda_fixa import RendaFixa, IOF_PERCENT
from services.renda_fixa_factory import RendaFixaFactory

class TestFreeTaxRendaFixa(unittest.TestCase):

    def setUp(self):        
        self.renda_fixa_factory = RendaFixaFactory()
        return super().setUp()

    def test_initial_value(self):
        start_date = datetime(2025, 1, 1, 0, 0, 0, 0)
        interest = 10.0
        maturity = start_date.date() + relativedelta(years=2)
        renda_fixa = self.renda_fixa_factory.lci(1000,interest,start_date, maturity)
    
        self.assertEqual(renda_fixa.net_value(start_date.date()), 1000)
        self.assertEqual(renda_fixa.tax_iof_value(start_date.date()), 0)
        self.assertEqual(renda_fixa.gross_value(start_date.date()), 1000)

    def test_count_business_days(self):
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 12, 31)

        count_business_days = RendaFixa.count_business_days(start_date, end_date)
        self.assertEqual(count_business_days, 261)

    def test_daily_interest_percent(self):
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 12, 31)
        interest = 0.1
        decimal_places = 5
        self.assertAlmostEqual(RendaFixa.daily_interest_percent(
            interest, start_date, end_date
        ), 0.00036523978, decimal_places)

    def test_net_return(self):
        start_date = datetime(2025, 1, 1)
        maturity = date(2027, 1, 1)
        start_value = 1000
        interest = 0.10
        renda_fixa = self.renda_fixa_factory.lci(start_value,interest,start_date, maturity)

        # TODO: this should be equal
        self.assertAlmostEqual(
            start_value * (interest + 1),
            renda_fixa.gross_value(
                date(2026, 1, 1)
            )
        )
        self.assertAlmostEqual(
            0,
            renda_fixa.tax_iof_value(
                date(2026, 1, 1)
            )
        ), 10
        
    def test_value_after_maturity_date(self):
        start_date = datetime(2025, 1, 1)
        maturity = date(2027, 1, 1)
        start_value = 1000
        interest = 0.10
        renda_fixa = self.renda_fixa_factory.lci(start_value,interest,start_date, maturity)

        self.assertAlmostEqual(
            start_value * (interest + 1) ** 2,
            renda_fixa.gross_value(
                date(9999, 1, 1)
            ), 10
        )
        
if __name__ == '__main__':
    unittest.main()