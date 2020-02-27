import subprocess
import time
import gzip, shutil
import datetime
import json
import csv
import sys
from pandas import read_csv
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARIMAResults
from random import random
def __getnewargs__(self):
    return ((self.endog),(self.k_lags, self.k_diff, self.k_ma))
ARIMA.__getnewargs__ = __getnewargs__

# if not sys.warnoptions:
#     import warnings
#     warnings.simplefilter("ignore")

input_len = 12

#Read json file
with open("sensors_speed.json") as f:
    output_sensor_speeds = json.load(f)
    print(output_sensor_speeds.keys())


starttime = time.time()
while True:
    with open('sensors_speed.json') as f:
        sensors_dict = json.load(f)
    currentTime = datetime.datetime.now()
    tenMinAgo = datetime.datetime.now() - datetime.timedelta(minutes = input_len * 2)
    tenMinLater = datetime.datetime.now() + datetime.timedelta(minutes = input_len * 2)
    currentStr = '{:%Y-%m-%d %H:%M:%S}'.format(currentTime)
    tenMinStr = '{:%Y-%m-%d %H:%M:%S}'.format(tenMinAgo)
    tenMinLatStr = '{:%Y-%m-%d %H:%M:%S}'.format(tenMinLater)
    # Format: 2020-01-25 12:00:00
    print('++++++++++++++++++++++')
    subprocess.call(["psql", "-U", "adms-api", "-d", "adms", "-h", "gd.usc.edu", "-p", "5433", "-c", "COPY (SELECT link_id, date_and_time, speed FROM congestion.congestion_data WHERE date_and_time BETWEEN '" + tenMinStr + "' AND '" + currentStr + "') TO stdout DELIMITER \',\' CSV HEADER ", ">", "C:\\Users\\namju\\OneDrive\\Documents\\GitHub\\imsc_sensor_speed\\production\\temp.csv"], shell=True)
    print('-----------------------')
    idList = sensors_dict.keys()

    speed_values= {}

    with open('production/temp.csv', 'rt') as f:
        mycsv = csv.reader(l.replace('\0', '') for l in f)
        count = 0
        for row in mycsv:
            if count == 0 or row == []:
                count = 1
                continue
            link_id = row[0]
            speed = float(row[2])
            if link_id in idList:
                if link_id not in speed_values:
                    speed_values[link_id] = [speed+random()]
                else:
                    speed_values[link_id].append(speed+random()) 
        for link_id in speed_values:
            speed_values[link_id].reverse()

    url = 'http://imscgpu.usc.edu:8999/v1/models/dcrnn:predict'

    headers = {
        'Content-type' : 'application/json',
        'Charset' : 'UTF-8'
    }
        
    output_sensor_speeds = requests.post(url = url, 
    json = {'instances':temp_values.tolist()}, headers = headers)
        
    #write back to json file
    #print(output_sensor_speeds)
    with open("sensors_speed2.json", "w") as f:
        json.dump(output_sensor_speeds, f)
    time.sleep(120.0 - ((time.time() - starttime) % 60.0))