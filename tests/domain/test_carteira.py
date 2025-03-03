import unittest
from datetime import datetime
from domain.wallet import Wallet

class TestWallet(unittest.TestCase):
    def test_initial_value(self):
        wallet = Wallet()
        self.assertEqual(wallet.net_value(datetime.now()), 0)
        self.assertEqual(wallet.tax_value(datetime.now()), 0)
        self.assertEqual(wallet.brut_value(datetime.now()), 0)

    def test_deposit(self):
        wallet = Wallet()
        today = datetime(2025, 1, 1)
        wallet.deposit(10, today)

        self.assertEqual(wallet.net_value(today), 10)
        self.assertEqual(wallet.tax_value(today), 0)
        self.assertEqual(wallet.brut_value(today), 10)

        yesterday = datetime(2024, 12, 31)
        self.assertEqual(wallet.net_value(yesterday), 0)
        self.assertEqual(wallet.tax_value(yesterday), 0)
        self.assertEqual(wallet.brut_value(yesterday), 0)

    def test_withdraw(self):
        wallet = Wallet()
        yesterday = datetime(2024, 12, 31)
        today = datetime(2025, 1, 1)
        tomorrow = datetime(2025, 1, 2)
        wallet.deposit(10, today)
        wallet.withdraw(8, tomorrow)

        self.assertEqual(wallet.net_value(yesterday), 0)
        self.assertEqual(wallet.net_value(today), 10)
        self.assertEqual(wallet.net_value(tomorrow), 2)

        

if __name__ == '__main__':
    unittest.main()