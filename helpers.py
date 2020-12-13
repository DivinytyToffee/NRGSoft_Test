import json

import numpy as np
import pandas as pd


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


def mongo_record(data):
    series = pd.Series(data)
    series.index = pd.DatetimeIndex(series.index)
    if series.dtype != np.float64:
        if series.dtype != np.int64:
            print(series.dtype)
            raise WrongDataTypeException

    insert = series.to_json(orient='index')
    return json.loads(insert)


class WrongDataTypeException(BaseException):
    def __str__(self):
        return "Wrong data type"