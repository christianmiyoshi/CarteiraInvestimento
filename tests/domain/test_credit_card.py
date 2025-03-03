import unittest
from datetime import date
from domain.credit_card import CreditCard
from domain.payment_installment import PaymentInstallment

class TestCreditCard(unittest.TestCase):
    def test_simple_payment(self):
        today = date(2025, 1, 1)
        monthly_value = 100
        number_installments = 10        
        installment = PaymentInstallment(
            today, monthly_value, number_installments
        )
        card = CreditCard(15)
        card.add_payment_installment(installment)

        assert len(card.deposits()) == 10

    def test_simple_payment_deposits(self):
        today = date(2025, 1, 1)   

        monthly_value = 100
        number_installments = 1

        installment = PaymentInstallment(
            today, monthly_value, number_installments
        )
        card = CreditCard(15)
        card.add_payment_installment(installment)

        self.assertEqual(card.result(today), 0)

        payment_date = date(2025, 1, 15)
        self.assertEqual(card.result(payment_date), -100)




if __name__ == '__main__':
    unittest.main()