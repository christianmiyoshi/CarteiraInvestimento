import unittest
from datetime import datetime, date
from domain.indice import Indice, RangedIndex
from domain.payment_installment import PaymentInstallment

class TestIndice(unittest.TestCase):
    def test_simple_indice(self):
        indice = RangedIndex("SELIC")
        indice.add_intereset(date(2020, 1, 1), 0.10)
        indice.add_intereset(date(2025, 1, 1), 0.15)
        indice.add_intereset(date(2025, 2, 1), 0.20)

        self.assertEqual(0.10, indice.get_year_interest_at(date(2024, 12, 31)))
        self.assertEqual(0.15, indice.get_year_interest_at(date(2025, 1, 1)))
        self.assertEqual(0.15, indice.get_year_interest_at(date(2025, 1, 31)))
        self.assertEqual(0, indice.get_year_interest_at(date(2025, 2, 1)))
        self.assertEqual(0, indice.get_year_interest_at(date(2025, 2, 2)))
        self.assertEqual(0.20, indice.get_year_interest_at(date(2025, 2, 3)))