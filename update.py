import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sklearn.metrics import mean_squared_error
from pandas import read_csv
from pandas import datetime
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

def parser(x):
	return datetime.strptime('120'+x, '%Y-%m')

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    logitude = db.Column(db.Float, unique=False, nullable = False)
    latitude = db.Column(db.Float, unique=False, nullable = False)

    def __repr__(self):
        return super().__repr__()   

# Change the querying statements
Sensor.query.all()
 
 # Need temp file to store the past history of 2 minutes
series = read_csv('sensor_speed.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
X = series.values
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()

for t in range(len(test)):
	model = ARIMA(history, order=(5,1,0))
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test[t]
	history.append(obs)
	print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)

pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()

# Write on the csv file later
filename = "sensor_speed.csv"

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    csvwriter.writerow(fields)

    csvwriter.writerows(rows)

# Update temp file here