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
import os
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
    query_command = """psql -U adms-api -d adms -h gd.usc.edu -p 5433 -c "COPY (SELECT link_id, date_and_time, speed from congestion.congestion_data WHERE date_and_time BETWEEN '"""+ tenMinStr + "' AND '"+ currentStr +"""') TO stdout CSV HEADER" > temp.csv"""
    print(query_command)
    print('++++++++++++++++++++++')
    # subprocess.call(["psql", "-U", "adms-api", "-d", "adms", "-h", "gd.usc.edu", "-p", "5433", "-c", "COPY (SELECT link_id, date_and_time, speed FROM congestion.congestion_data WHERE date_and_time BETWEEN '" + tenMinStr + "' AND '" + currentStr + "') TO stdout DELIMITER \',\' CSV HEADER ", ">", "C:\\Users\\namju\\OneDrive\\Documents\\GitHub\\imsc_sensor_speed\\production\\temp.csv"], shell=True)
    os.system(query_command)
    print('-----------------------')
    idList = sensors_dict.keys()

    speed_values= {}

    with open('temp.csv', 'rt') as f:
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

    count = 0
    count2 = 0
    for idx, link_id in enumerate(speed_values):
        print("Finished ", idx, " out of ", len(speed_values))
        X = speed_values[link_id]
        # if idx == 10:
        #     break
        for i in range(input_len):
            try:
                #Update current value
                output_sensor_speeds[link_id]['speed'] = X[-1]
                #print(X)

                order = (2, 1, 0)
                model = ARIMA(X, order)
                fit = model.fit(disp=0)

                output = fit.forecast()
                # print("i = ", i)
                # print("Output = ", output[0].tolist()[0])
                if (output[0][-1] < 0):
                    output[0][-1] = 0
                    output[0][-2] = 0
                output_sensor_speeds[link_id]['speed_'+str(i)] = float(output[0].tolist()[0])
                X.append(output[0].tolist()[0])
                # count2 +=1
                # print("count2=", count2)
            except:
                output = X[-1] + random()
                output_sensor_speeds[link_id]['speed_'+str(i)] = output
                count +=1
                print("count = ", count)
                X.append(output)
            

        
    #write back to json file
    #print(output_sensor_speeds)
    with open("sensors_speed.json", "w") as f:
        json.dump(output_sensor_speeds, f)
    print("Finishing dumping file")
    time.sleep(120.0 - ((time.time() - starttime) % 60.0))