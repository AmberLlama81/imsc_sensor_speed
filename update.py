import json
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error
from pandas import read_csv
from pandas import datetime
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot

db_string = "postgresql://adms-api:V^YDiwdR&VvM@localhost/PostgreSQL"

db = create_engine(db_string)

# Change the querying statements
query_result = db.execute("SELECT link_id, start_location.lat, start_location.lng FROM congestion_inventory")

# Need temp file to store the past history of 2 minutes
print(type(query_result))
temp = 


# Run ARIMA model

# Write on the json file later

# Update temp file here