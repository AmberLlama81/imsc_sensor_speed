import subprocess
import time
import gzip, shutil
import datetime
import json
import csv
from pandas import read_csv
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARIMAResults

def __getnewargs__(self):
    return ((self.endog),(self.k_lags, self.k_diff, self.k_ma))
ARIMA.__getnewargs__ = __getnewargs__

starttime = time.time()
while True:
    with open('sensors_speed.json') as f:
        sensors_dict = json.load(f)
    currentTime = datetime.datetime.now()
    tenMinAgo = datetime.datetime.now() - datetime.timedelta(minutes=10)
    currentStr = '{:%Y-%m-%d %H:%M:%S}'.format(currentTime)
    tenMinStr = '{:%Y-%m-%d %H:%M:%S}'.format(tenMinAgo)
    # Format: 2020-01-25 12:00:00
    subprocess.call("psql -U adms-api -d adms -h gd.usc.edu -p 5433 -c ""COPY (SELECT link_id, date_and_time, speed FROM congestion.congestion_data WHERE date_and_time BETWEEN '"+ tenMinStr + "' AND '" + currentStr + "') TO stdout DELIMITER ',' CSV HEADER"" \ | gzip > temp.csv.gz")
    with gzip.open('temp.csv.gz', 'r') as f_in, open('temp.csv', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    idList = sensors_dict.keys()

    speed_values= {}

    with open('temp.csv' 'rb') as f:
        mycsv = csv.reader(f)
        for row in mycsv:
            link_id = row[0]
            speed = float(row[2])
            if link_id in idList:
                if link_id not in speed_values:
                    speed_values[link_id] = [speed]
                else:
                    speed_values[link_id].append(speed) 
        for link_id in speed_values:
            speed_values[link_id].reverse()

    for link_id in speed_values:
        X = speed_values[link_id]

        X = X.astype('float32')

        model = ARIMA(X, order = (1, 1, 1))
        model_fit = model.fit()



    time.sleep(120.0 - ((time.time() - starttime) % 60.0))