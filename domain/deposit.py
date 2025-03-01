import datetime

class Deposit:
    def __init__(self, value: float, timestamp: datetime.datetime):
        self._value = value
        self._timestamp = timestamp 

    @property
    def value(self) -> float:
        return self._value

    @property
    def timestamp(self) -> datetime.datetime:
        return self._timestamp

    def value_at(self, timestamp: datetime.datetime) -> float:
        if self.timestamp <= timestamp:
            return self.value

        return 0
