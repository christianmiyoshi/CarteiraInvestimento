import unittest
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from domain.index import RangedIndex
from domain.renda_fixa import RendaFixa, IOF_PERCENT
from services.renda_fixa_factory import RendaFixaFactory

class TestRendaFixaIndice(unittest.TestCase):

    def setUp(self):        
        self.renda_fixa_factory = RendaFixaFactory()
        return super().setUp()

    def test_simple_ldi_no_fixed_income(self):
        indice = RangedIndex("CDI")
        indice.add_intereset(date(2025, 1, 1), 0.1)

        start_date = datetime(2025, 1, 1, 0, 0, 0, 0)        
        maturity = start_date.date() + relativedelta(years=2)
        renda_fixa = self.renda_fixa_factory.lci_floating_rate(1000, 0, start_date, maturity, indice)
    
        self.assertEqual(renda_fixa.net_value(start_date.date()), 1000)
        self.assertEqual(renda_fixa.tax_iof_value(start_date.date()), 0)
        self.assertEqual(renda_fixa.gross_value(start_date.date()), 1000)

        self.assertAlmostEqual(renda_fixa.net_value(date(2026, 1, 1)), 1100)
        self.assertAlmostEqual(renda_fixa.tax_iof_value(date(2026, 1, 1)), 0)
        self.assertAlmostEqual(renda_fixa.gross_value(date(2026, 1, 1)), 1100)

    def test_simple_ldi_and_fixed_income(self):
        indice = RangedIndex("CDI")
        indice.add_intereset(date(2025, 1, 1), 0.08)

        start_date = datetime(2025, 1, 1, 0, 0, 0, 0)        
        maturity = start_date.date() + relativedelta(years=2)
        renda_fixa = self.renda_fixa_factory.lci_floating_rate(1000, 0.02, start_date, maturity, indice)
    
        self.assertEqual(renda_fixa.net_value(start_date.date()), 1000)
        self.assertEqual(renda_fixa.tax_iof_value(start_date.date()), 0)
        self.assertEqual(renda_fixa.gross_value(start_date.date()), 1000)

        self.assertAlmostEqual(renda_fixa.net_value(date(2026, 1, 1)), 1100)
        self.assertAlmostEqual(renda_fixa.tax_iof_value(date(2026, 1, 1)), 0)
        self.assertAlmostEqual(renda_fixa.gross_value(date(2026, 1, 1)), 1100)

        
if __name__ == '__main__':
    unittest.main()