import datetime

from domain.deposit import Deposit
from domain.payment_installment import PaymentInstallment
from domain.renda_fixa import RendaFixa

class FixIncome(Deposit):
    def __init__(self, value: float, timestamp: datetime.datetime):
        self._value = value
        self._timestamp = timestamp
        self.day = timestamp.day
        assert self.day <= 28

    @property
    def value(self) -> float:
        return self._value

    @property
    def timestamp(self) -> datetime.datetime:
        return self._timestamp

    def value_at(self, timestamp: datetime.datetime) -> float:
        if self.timestamp > timestamp:
            return 0

        number_months = PaymentInstallment.diff_months(timestamp.date(), self.timestamp) + 1
        return number_months * self._value
