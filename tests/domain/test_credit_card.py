import unittest
from datetime import datetime, date
from domain.credit_card import CreditCard
from domain.payment_installment import PaymentInstallment

class TestCreditCard(unittest.TestCase):
    def test_simple_payment(self):
        today = datetime(2025, 1, 1)
        monthly_value = 100
        number_installments = 10        
        installment = PaymentInstallment(
            today, monthly_value, number_installments
        )
        card = CreditCard(15)
        card.add_payment_installment(installment)

        assert len(card.debts) == 10

    def test_simple_payment(self):
        today = date(2025, 1, 1)   

        monthly_value = 100
        number_installments = 1

        installment = PaymentInstallment(
            today, monthly_value, number_installments
        )
        card = CreditCard(15)
        card.add_payment_installment(installment)

        assert card.total_debt(today) == 100
        assert card.result(today) == 0

        payment_date = date(2025, 1, 15)
        assert card.total_debt(today) == 100
        assert card.result(payment_date) == -100

        card.pay(100, payment_date)
        assert card.total_debt(payment_date) == 100
        assert card.total_payment(payment_date) == 100
        assert card.result(payment_date) == 0



if __name__ == '__main__':
    unittest.main()