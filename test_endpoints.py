import os

import requests

from main import app

os.environ['NO_PROXY'] = '127.0.0.1'

host = app.config.get('HOST')
port = app.config.get('PORT')
url = f"http://{host}:{port}/time-series"


class TestEndpoint:

    # def __init__(self):
    #     self.id = None

    def test_first(self):
        p = requests.post(f"http://{host[0]}:{port[0]}/time-series", data={
            'data': {'456': 89, 789: 56}
        })

        assert isinstance(1, float)


if __name__ == '__main__':
    p = requests.post(url=url, data={
        'data': {'2000-02-03': 89}
    })
    a = p.status_code
    print(p)

