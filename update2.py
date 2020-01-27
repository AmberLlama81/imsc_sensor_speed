import subprocess
import time
import datetime

starttime = time.time()
while True:
    currentTime = datetime.datetime.now()
    twoMinAgo = datetime.datetime.now() - datetime.timedelta(minutes=2)
    currentStr = '{:%Y-%m-%d %H:%M:%S}'.format(currentTime)
    twoMinStr = '{:%Y-%m-%d %H:%M:%S}'.format(twoMinAgo)
    # Format: 2020-01-25 12:00:00
    subprocess.call("psql -U adms-api -d adms -h gd.usc.edu -p 5433 -c ""COPY (SELECT link_id, date_and_time, speed FROM congestion.congestion_data WHERE date_and_time BETWEEN '"+ twoMinStr + "' AND '" + currentStr + "') TO stdout DELIMITER ',' CSV HEADER"" \ | gzip > sensors_speed.csv.gz")
    time.sleep(120.0 - ((time.time() - starttime) % 60.0))