import unittest
from datetime import date, datetime, timedelta
from domain.credit_card import CreditCard
from domain.payment_installment import PaymentInstallment
from domain.wallet import Wallet
from services.renda_fixa_factory import RendaFixaFactory

class TestCreditCard(unittest.TestCase):
    def setUp(self):        
        self.renda_fixa_factory = RendaFixaFactory()
        return super().setUp()


    def test_simulate_installment(self):
        today = date(2025, 1, 1)

        monthly_value = 90
        number_installments = 10        
        installment = PaymentInstallment(
            today, monthly_value, number_installments
        )
        card = CreditCard(payment_day=15)
        card.add_payment_installment(installment)
        wallet = Wallet()
        wallet.add_credit_card(card)
        wallet.deposit(monthly_value * number_installments, datetime(2025, 1, 15, 0, 0))

        start_date = datetime(2025, 1, 15)
        maturity = date(2025, 10, 15)
        cashback_value = monthly_value * number_installments
        interest = 0.10
        lci = self.renda_fixa_factory.lci_liquidity(cashback_value,interest,start_date, maturity)
        wallet.invest(lci)
        for i in range(number_installments):
            lci.withdraw(monthly_value, date(2025, i + 1, 15))

        # cashback
        start_date = datetime(2025, 1, 15)
        maturity = date(2025, 10, 15)
        cashback_value = monthly_value * number_installments * 0.01
        
        interest = 0.20
        wallet.deposit(cashback_value, datetime(2025, 1, 15, 0, 0))
        lci_cashback = self.renda_fixa_factory.cdb_liquidity(cashback_value,interest,start_date, maturity)
        wallet.invest(lci_cashback)


        # print('result')
        # start = date(2025, 1, 1)
        # end = date(2025, 11, 1)
        # for i in range((end - start).days):
        #     current_date = start + timedelta(days=i)
        #     print(current_date, "%.4f" % wallet.brut_value(current_date))

    def test_simulate_cash(self):
        today = date(2025, 1, 1)

        value = 900
        discout = 0.10

        discounted_value = value * (1 - discout)
        number_installments = 1 
        installment = PaymentInstallment(
            today, discounted_value, number_installments
        )

        card = CreditCard(payment_day=15)
        card.add_payment_installment(installment)
        wallet = Wallet()
        wallet.add_credit_card(card)

        wallet.deposit(value, datetime(2025, 1, 15, 0, 0))

        start_date = datetime(2025, 1, 15)
        maturity = date(2025, 10, 15)
        start_value = value - discounted_value
        interest = 0.10
        lci = self.renda_fixa_factory.lci_liquidity(start_value,interest,start_date, maturity)
        wallet.invest(lci)

        # print('result')
        # start = date(2025, 1, 1)
        # end = date(2025, 11, 1)
        # for i in range((end - start).days):
        #     current_date = start + timedelta(days=i)
        #     print(current_date, "%.4f" % wallet.brut_value(current_date))