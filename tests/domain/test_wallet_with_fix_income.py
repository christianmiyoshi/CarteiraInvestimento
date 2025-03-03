import unittest
from datetime import datetime, date
from domain.carteira import Wallet
from domain.credit_card import CreditCard
from domain.fix_income import FixIncome
from domain.payment_installment import PaymentInstallment

class TestWalletWithFxIncome(unittest.TestCase):
    def test_simple_income(self):
        today = datetime(2025, 1, 1)      
        wallet = Wallet()

        salary = FixIncome(1000, today)
        wallet.add_deposit(salary)

        self.assertEqual(1000, wallet.brut_value(today))
        self.assertEqual(2000, wallet.brut_value(datetime(2025, 2, 1) ))
        self.assertEqual(3000, wallet.brut_value(datetime(2025, 3, 1) ))

if __name__ == '__main__':
    unittest.main()