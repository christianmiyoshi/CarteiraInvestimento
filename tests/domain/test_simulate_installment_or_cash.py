import unittest
from datetime import date, timedelta
from domain.credit_card import CreditCard
from domain.payment_installment import PaymentInstallment
from domain.wallet import Wallet

class TestCreditCard(unittest.TestCase):
    def test_simulate_installment(self):
        today = date(2025, 1, 1)

        monthly_value = 1000
        number_installments = 10        
        installment = PaymentInstallment(
            today, monthly_value, number_installments
        )
        card = CreditCard(payment_day=1)
        card.add_payment_installment(installment)
        walletInstallment = Wallet()
        walletInstallment.add_credit_card(card)

        print('result')
        start = date(2025, 1, 1)
        end = date(2025, 12, 1)
        for i in range((end - start).days):
            current_date = start + timedelta(days=i)
            print(current_date, walletInstallment.brut_value(current_date))
