# imsc_sensor_speed

imsc_sensor_speed$ psql -U adms-api -d adms -h gd.usc.edu -p 5433 -c "COPY (SELECT link_id, date_and_time, speed FROM congestion.congestion_data WHERE date_and_time BETWEEN '2020-01-25 12:00:00' AND '2020-01-25 15:52:00') TO stdout DELIMITER ',' CSV HEADER" \ | gzip > sensors_spped.csv.gz 
