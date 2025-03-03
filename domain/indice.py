from datetime import date


class InterestDate:
    def __init__(self, date: date, interest: float):
        self.date = date
        self.interest = interest

class Indice:
    def __init__(self, name: str):
        self.name = name
        self.interest_list: list[InterestDate] = []

    def add_intereset(self, date: date, interest: float):
        self.interest_list.append(
            InterestDate(date, interest)
        )
        self.interest_list.sort(key=lambda interest: interest.date)

    def get_interest_at(self, date: date):
        filtered_items = [item for item in self.interest_list if item.date <= date]
        if not filtered_items:
            return 0
        return max(filtered_items, key=lambda x: x.date).interest