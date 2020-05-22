import subprocess
import time
import gzip, shutil
import datetime
import json
import csv
import sys
import requests
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARIMAResults
from random import random
import os
def __getnewargs__(self):
    return ((self.endog),(self.k_lags, self.k_diff, self.k_ma))
ARIMA.__getnewargs__ = __getnewargs__

# if not sys.warnoptions:
#     import warnings
#     warnings.simplefilter("ignore")

input_len = 12

currentTime = datetime.datetime.now()
weekAgo = datetime.datetime.now() - datetime.timedelta(days = 7)
currentStr = '{:%Y-%m-%d %H:%M:%S}'.format(currentTime)
weekStr = '{:%Y-%m-%d %H:%M:%S}'.format(weekAgo)
# Format: 2020-01-25 12:00:00
query_command = """psql -U adms-api -d adms -h gd.usc.edu -p 5433 -c "COPY (SELECT date_and_time, bus_id, line_id, run_id, route_id, route_description, bus_direction, st_x(bus_location), st_y(bus_location), bus_location_time, schedule_deviation, next_stop_time, next_stop_location, next_stop_scheduled_time from transit.bus_data WHERE date_and_time BETWEEN '"""+ weekStr + "' AND '"+ currentStr +"""') TO stdout CSV HEADER" > temp.csv"""
print(query_command)
print('++++++++++++++++++++++')
os.system(query_command)
print('-----------------------')


with open('temp.csv', 'r') as source:
        rdr = csv.reader(source)
        with open('bus51.csv', 'w') as result:
            wtr = csv.writer(result)
            for r in rdr:
                if r[6] == 'SOUTH':
                    r[6] = 1
                elif r[6] == 'EAST':
                    r[6] = 2
                elif r[6] == 'WEST':
                    r[6] = 3
                elif r[6] == 'NORTH':
                    r[6] = 4 
                else:
                    r[6] = 0
                wtr.writerow(r)