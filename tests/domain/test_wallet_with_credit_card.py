import unittest
from datetime import datetime, date
from domain.wallet import Wallet
from domain.credit_card import CreditCard
from domain.payment_installment import PaymentInstallment

class TestWalletWithCreditCard(unittest.TestCase):
    def test_simple_installment(self):
        today = date(2025, 1, 1)        
        wallet = Wallet()

        card = CreditCard(15)
        wallet.add_credit_card(card)

        monthly_value = 100
        number_installments = 1
        payment = PaymentInstallment(
            today,
            monthly_value,
            number_installments
        )      

        card.add_payment_installment(payment)
        self.assertEqual(-100, wallet.brut_value(datetime(2025, 1, 15)))

        wallet.deposit(100, datetime(2025, 1, 15))
        self.assertEqual(0, wallet.brut_value(datetime(2025, 1, 15)))

    def test_payment_two_installment(self):
        today = date(2025, 1, 1)        
        wallet = Wallet()

        card = CreditCard(15)
        wallet.add_credit_card(card)

        monthly_value = 100
        number_installments = 2
        payment = PaymentInstallment(
            today,
            monthly_value,
            number_installments
        )      
        card.add_payment_installment(payment)
        wallet.deposit(200, datetime(2025, 1, 14))
        
        self.assertEqual(200, wallet.brut_value(date(2025, 1, 14)))
        self.assertEqual(100, wallet.brut_value(date(2025, 1, 15)))

        self.assertEqual(100, wallet.brut_value(date(2025, 2, 14)))
        self.assertEqual(0, wallet.brut_value(datetime(2025, 2, 15)))


if __name__ == '__main__':
    unittest.main()