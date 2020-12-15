NRGSoft_Test

Install:

1. Install mongoDB - for collect data
2. Install requirements from requirements.txt
3. run Flask application on `main.py`

Requests:

endpoint name - `/time-series`

# POST

Method for send time-series data.

Send json as `{"data": {"yyy-mm-dd": <number>}}`. 

Key must any calendar format.

return `{"id": <string>}`

# GET

Method for calculate cagr.

Send json as `{"id": <string>}`. 

return `{"cagr": <int>}`

# PUT

Method for extend time-series data.

Send json as `{"id": <string>, "data": {"yyy-mm-dd": <number>}}`. 

return `NO DATA
