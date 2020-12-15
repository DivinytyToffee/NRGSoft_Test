import os

import requests

from main import app
import numpy as np
import datetime
from datetime import timedelta

os.environ['NO_PROXY'] = '127.0.0.1'

host = app.config.get('HOST')
port = app.config.get('PORT')
url = f"http://{host}:{port}/time-series"


class TestEndpoint:

    _id = None

    @staticmethod
    def gen_series():
        count = 3650
        start_date = datetime.date(2010, 1, 1)
        date_index = [str(start_date + timedelta(days=i))for i in range(count)]

        price = 100
        prices = []
        for i in range(count):
            price *= (1 + np.random.normal(loc=0.0001, scale=0.005))
            prices.append(price)

        series = dict(zip(date_index, prices))
        return series

    def test_first(self):
        p = requests.post(url, json={
            'data': {'456': 89, '789': 56}
        })

        assert p.status_code, 422

    def test_second(self):
        p = requests.post(url, json={
            'data': {'2018-02-03': 89, '2018-0396': 56}
        })

        assert p.status_code, 422

    def test_third(self):
        p = requests.post(url, json={
            'data': {'2018-02-03': 'test', '2018-03-06': '56'}
        })

        assert p.status_code, 422

    def test_fourth(self):
        p = requests.post(url, json={
            'data': {'157946760000000': 89, '157947760000000': 56}
        })

        assert p.status_code, 422

    def test_fifth(self):
        p = requests.post(url, json={
            'data': self.gen_series()
        })

        self._id = p.json().get("id")

        assert p.status_code, 200

    def test_sixth(self):
        new_id = self._id[:-1] + 'f'

        p = requests.get(url, json={"id": new_id})

        assert p.status_code, 422

    def test_seventh(self):
        new_id = self._id[:-5]

        p = requests.get(url, json={"id": new_id})

        assert p.status_code, 404

    def test_eighth(self):
        p0 = requests.post(url, json={
            'data': {'2018-02-03': 25}
        })

        _id = p0.json().get('id')

        p = requests.get(url, json={"id": _id})

        assert p.status_code, 400

    def test_ninth(self):
        p = requests.get(url, json={"id": 0})

        assert p.status_code, 422

    def test_tenth(self):
        p = requests.get(url, json={"id": self._id})

        assert p.status_code, 200

    def test_eleventh(self):
        p = requests.get(url, json={"id": self._id})

        assert p.status_code, 200

    def test_twelfth(self):
        new_id = self._id[:-5]

        p = requests.put(url, json={"id": new_id, 'data': {'2018-02-03': 25}})

        assert p.status_code, 404

    def test_thirteenth(self):
        p = requests.put(url, json={
            "id": self._id,
            'data': {'456': 89, '789': 56}
        })

        assert p.status_code, 422

    def test_fourteenth(self):
        p = requests.put(url, json={
            "id": self._id,
            'data': {'2018-02-03': 89, '2018-0396': 56}
        })

        assert p.status_code, 422

    def test_fifteenth(self):
        p = requests.put(url, json={
            "id": self._id,
            'data': {'2018-02-03': 'test', '2018-03-06': '56'}
        })

        assert p.status_code, 422

    def test_sixteenth(self):
        p = requests.put(url, json={
            "id": self._id,
            'data': {'157946760000000': 89, '157947760000000': 56}
        })

        assert p.status_code, 422

    def test_seventeenth(self):
        new_id = self._id[:-1] + 'f'

        p = requests.put(url, json={
            "id": new_id,
            'data': {'2018-02-03': 25}
        })

        assert p.status_code, 422

    def test_eighteenth(self):
        p = requests.put(url, json={
            "id": self._id,
            'data': {'2018-02-03': 25}
        })

        assert p.status_code, 204


