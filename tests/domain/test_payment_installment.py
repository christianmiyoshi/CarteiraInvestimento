import unittest
from datetime import datetime
from domain.payment_installment import PaymentInstallment

class TestPaymentInstallment(unittest.TestCase):
    def test_initial_value(self):
        today = datetime(2025, 1, 1)
        monthly_value = 100
        number_installments = 10
        payment = PaymentInstallment(
            today,
            monthly_value,
            number_installments
        )

        assert payment.paid_value() == 0

    def test_pay(self):
        today = datetime(2025, 1, 1)
        monthly_value = 100
        number_installments = 10
        payment = PaymentInstallment(
            today,
            monthly_value,
            number_installments
        )
        payment.pay()
        payment.pay()

        assert payment.paid_value() == 2 * monthly_value
        assert payment.debt() == (number_installments - 2) * monthly_value

    def test_pay_up_to_date(self):
        today = datetime(2025, 1, 1)
        monthly_value = 100
        number_installments = 10
        payment = PaymentInstallment(
            today,
            monthly_value,
            number_installments
        )

        payment.pay_up_to_date(datetime(2024, 12, 31))
        assert payment.paid_value() == 0

        payment.pay_up_to_date(datetime(2025, 1, 1))
        assert payment.paid_value() == 1 * monthly_value

        payment.pay_up_to_date(datetime(2025, 1, 31))
        assert payment.paid_value() == 1 * monthly_value

        payment.pay_up_to_date(datetime(2025, 2, 1))
        assert payment.paid_value() == 2 * monthly_value
        

if __name__ == '__main__':
    unittest.main()