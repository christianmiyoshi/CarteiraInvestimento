import unittest
from datetime import datetime, date
from domain.wallet import Wallet
from domain.credit_card import CreditCard
from domain.fix_income import FixIncome
from domain.payment_installment import PaymentInstallment
from services.renda_fixa_factory import RendaFixaFactory

class TestWalletWithRendaFixa(unittest.TestCase):
    def setUp(self):        
        self.renda_fixa_factory = RendaFixaFactory()
        return super().setUp()
    
    def test_simple_cdb(self):
        todaytime = datetime(2025, 1, 1)      
        wallet = Wallet()
        wallet.deposit(1000, todaytime)

        start_date = datetime(2025, 1, 1)
        maturity = date(2027, 1, 1)
        start_value = 1000
        interest = 0.10
        renda_fixa = self.renda_fixa_factory.cdb(start_value, interest, start_date, maturity)
        wallet.invest(renda_fixa)

        self.assertEqual(0, wallet.brut_value(start_date))
        self.assertEqual(0, wallet.brut_value(date(2026, 12, 31)))

        gross_return = 1000 * (1 + 0.1) ** 2
        tax = (gross_return - start_value) * 0.15
        expected_income = gross_return - tax

        self.assertAlmostEqual(expected_income, wallet.brut_value(date(2027, 1, 1)), 10)

    def test_simple_lci(self):
        todaytime = datetime(2025, 1, 1)      
        wallet = Wallet()
        wallet.deposit(1000, todaytime)

        start_date = datetime(2025, 1, 1)
        maturity = date(2027, 1, 1)
        start_value = 1000
        interest = 0.10
        renda_fixa = self.renda_fixa_factory.lci(start_value, interest, start_date, maturity)
        wallet.invest(renda_fixa)

        self.assertEqual(0, wallet.brut_value(start_date))
        self.assertEqual(0, wallet.brut_value(date(2026, 12, 31)))

        gross_return = 1000 * (1 + 0.1) ** 2

        self.assertAlmostEqual(gross_return, wallet.brut_value(date(2027, 1, 1)), 10)




if __name__ == '__main__':
    unittest.main()