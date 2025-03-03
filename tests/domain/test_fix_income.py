import unittest
from datetime import datetime, date
from domain.fix_income import FixIncome
from domain.payment_installment import PaymentInstallment

class TestPaymentInstallment(unittest.TestCase):
    def test_initial_value(self):
        today = datetime(2025, 1, 1)
        monthly_value = 1000
        income = FixIncome(            
            monthly_value,
            today,
        )

        self.assertEqual(1000, income.value_at(today))
        self.assertEqual(2000, income.value_at(datetime(2025, 2, 1)))
        self.assertEqual(3000, income.value_at(datetime(2025, 3, 1)))

if __name__ == '__main__':
    unittest.main()