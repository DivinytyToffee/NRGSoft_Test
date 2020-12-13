import json

import numpy as np
import pandas as pd
import datetime
from datetime import timedelta


def get_years_past(series: pd.Series):
    start_date = series.index[0]
    end_date = series.index[-1]
    return (end_date - start_date).days / 365.25


def calculate_cagr(series: pd.Series):
    start_price = series.iloc[0]
    end_price = series.iloc[-1]
    value_factor = end_price / start_price
    year_past = get_years_past(series)
    return (value_factor ** (1 / year_past)) - 1


count = 365

start_date = datetime.date(2020, 1, 1)
date_index = [str(start_date + timedelta(days=i)) for i in range(count)]
# date_index = pd.DatetimeIndex(start_date + timedelta(days=i) for i in range(count))

price = initial_price = 0
prices = []
for i in range(count):
    price *= (1 + np.random.normal(loc=0.0001, scale=0.005))
    prices.append(price)


ser = dict(zip(date_index, ["10" for x in range(count)]))
print(json.dumps(ser))
