import unittest
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from domain.renda_fixa import RendaFixa, IOF_PERCENT

VALUE = 1000
START_DATE = datetime(2025, 1, 1)
EXPECTED_INVESTMENT_RETURN = {
    0: {"iof_percent": 100, "date": '2025-01-01',  "business_days": 0, "return_percent": 1, "gros_value": 1000, "net_income": 0, "iof": 0},
    1: {"iof_percent": 96, "date": '2025-01-02',  "business_days": 1, "return_percent": 1.00036524, "gros_value": 1000.36524, "net_income": 0.365239787, "iof": 0.350630195},
    2: {"iof_percent": 93, "date": '2025-01-03',  "business_days": 2, "return_percent": 1.000730613, "gros_value": 1000.730613, "net_income": 0.730612973, "iof": 0.679470065},
    3: {"iof_percent": 90, "date": '2025-01-04',  "business_days": 2, "return_percent": 1.000730613, "gros_value": 1000.730613, "net_income": 0.730612973, "iof": 0.657551676},
    4: {"iof_percent": 86, "date": '2025-01-05',  "business_days": 2, "return_percent": 1.000730613, "gros_value": 1000.730613, "net_income": 0.730612973, "iof": 0.628327157},
    5: {"iof_percent": 83, "date": '2025-01-06',  "business_days": 3, "return_percent": 1.00109612, "gros_value": 1001.09612, "net_income": 1.096119609, "iof": 0.909779275},
    6: {"iof_percent": 80, "date": '2025-01-07',  "business_days": 4, "return_percent": 1.00146176, "gros_value": 1001.46176, "net_income": 1.461759742, "iof": 1.169407793},
    7: {"iof_percent": 76, "date": '2025-01-08',  "business_days": 5, "return_percent": 1.001827533, "gros_value": 1001.827533, "net_income": 1.827533421, "iof": 1.3889254},
    8: {"iof_percent": 73, "date": '2025-01-09',  "business_days": 6, "return_percent": 1.002193441, "gros_value": 1002.193441, "net_income": 2.193440695, "iof": 1.601211708},
    9: {"iof_percent": 70, "date": '2025-01-10',  "business_days": 7, "return_percent": 1.002559482, "gros_value": 1002.559482, "net_income": 2.559481614, "iof": 1.79163713},
    10: {"iof_percent": 66, "date": '2025-01-11',  "business_days": 7, "return_percent": 1.002559482, "gros_value": 1002.559482, "net_income": 2.559481614, "iof": 1.689257865},
    11: {"iof_percent": 63, "date": '2025-01-12',  "business_days": 7, "return_percent": 1.002559482, "gros_value": 1002.559482, "net_income": 2.559481614, "iof": 1.612473417},
    12: {"iof_percent": 60, "date": '2025-01-13',  "business_days": 8, "return_percent": 1.002925656, "gros_value": 1002.925656, "net_income": 2.925656225, "iof": 1.755393735},
    13: {"iof_percent": 56, "date": '2025-01-14',  "business_days": 9, "return_percent": 1.003291965, "gros_value": 1003.291965, "net_income": 3.291964577, "iof": 1.843500163},
    14: {"iof_percent": 53, "date": '2025-01-15',  "business_days": 10, "return_percent": 1.003658407, "gros_value": 1003.658407, "net_income": 3.65840672, "iof": 1.938955562},
    15: {"iof_percent": 50, "date": '2025-01-16',  "business_days": 11, "return_percent": 1.004024983, "gros_value": 1004.024983, "net_income": 4.024982702, "iof": 2.012491351},
    16: {"iof_percent": 46, "date": '2025-01-17',  "business_days": 12, "return_percent": 1.004391693, "gros_value": 1004.391693, "net_income": 4.391692573, "iof": 2.020178583},
    17: {"iof_percent": 43, "date": '2025-01-18',  "business_days": 12, "return_percent": 1.004391693, "gros_value": 1004.391693, "net_income": 4.391692573, "iof": 1.888427806},
    18: {"iof_percent": 40, "date": '2025-01-19',  "business_days": 12, "return_percent": 1.004391693, "gros_value": 1004.391693, "net_income": 4.391692573, "iof": 1.756677029},
    19: {"iof_percent": 36, "date": '2025-01-20',  "business_days": 13, "return_percent": 1.004758536, "gros_value": 1004.758536, "net_income": 4.75853638, "iof": 1.713073097},
    20: {"iof_percent": 33, "date": '2025-01-21',  "business_days": 14, "return_percent": 1.005125514, "gros_value": 1005.125514, "net_income": 5.125514173, "iof": 1.691419677},
    21: {"iof_percent": 30, "date": '2025-01-22',  "business_days": 15, "return_percent": 1.005492626, "gros_value": 1005.492626, "net_income": 5.492626002, "iof": 1.6477878},
    22: {"iof_percent": 26, "date": '2025-01-23',  "business_days": 16, "return_percent": 1.005859872, "gros_value": 1005.859872, "net_income": 5.859871914, "iof": 1.523566698},
    23: {"iof_percent": 23, "date": '2025-01-24',  "business_days": 17, "return_percent": 1.006227252, "gros_value": 1006.227252, "net_income": 6.227251959, "iof": 1.43226795},
    24: {"iof_percent": 20, "date": '2025-01-25',  "business_days": 17, "return_percent": 1.006227252, "gros_value": 1006.227252, "net_income": 6.227251959, "iof": 1.245450392},
    25: {"iof_percent": 16, "date": '2025-01-26',  "business_days": 17, "return_percent": 1.006227252, "gros_value": 1006.227252, "net_income": 6.227251959, "iof": 0.996360313},
    26: {"iof_percent": 13, "date": '2025-01-27',  "business_days": 18, "return_percent": 1.006594766, "gros_value": 1006.594766, "net_income": 6.594766185, "iof": 0.857319604},
    27: {"iof_percent": 10, "date": '2025-01-28',  "business_days": 19, "return_percent": 1.006962415, "gros_value": 1006.962415, "net_income": 6.962414643, "iof": 0.696241464},
    28: {"iof_percent": 6, "date": '2025-01-29',  "business_days": 20, "return_percent": 1.007330197, "gros_value": 1007.330197, "net_income": 7.33019738, "iof": 0.439811843},
    29: {"iof_percent": 3, "date": '2025-01-30',  "business_days": 21, "return_percent": 1.007698114, "gros_value": 1007.698114, "net_income": 7.698114446, "iof": 0.230943433},
    30: {"iof_percent": 0, "date": '2025-01-31',  "business_days": 22, "return_percent": 1.008066166, "gros_value": 1008.066166, "net_income": 8.066165891, "iof": 0}
}


class TestRendaFixa(unittest.TestCase):
    def test_iof_without_tax(self):
        start_date = datetime(2025, 1, 1)
        next_year = datetime(2026, 1, 1)
        maturity = datetime(2027, 1, 1)
        start_value = 1000
        interest = 0.10
        renda_fixa = RendaFixa(start_value,interest,start_date, maturity)

        interest_daily = RendaFixa.daily_interest_percent(
            interest,
            start_date,
            next_year
        )
        
        for i in range(0, 31):
            date = (start_date + relativedelta(days=i)).date()            
            expected_data = EXPECTED_INVESTMENT_RETURN[i]
            iof = renda_fixa.tax_value(date)
            self.assertAlmostEqual(expected_data['iof'], iof, 7, f'IOF incorrect for day {i}' )            

if __name__ == '__main__':
    unittest.main()