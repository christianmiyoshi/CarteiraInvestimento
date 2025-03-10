from abc import ABC, abstractmethod
from datetime import date

class TaxCalculator(ABC):
    @abstractmethod
    def aliquota(self, calendar_days: int):
        pass
    
    @abstractmethod    
    def calculate(self, renda_fixa, timestamp: date): # TODO:"fix circular dependency"
        pass

        
