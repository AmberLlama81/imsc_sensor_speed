import requests
import json
import numpy as np

temp_values = np.random.rand(12,207,2)
print(temp_values.shape)

url = 'http://imscgpu.usc.edu:8999/v1/models/dcrnn:predict'

headers = {
    'Content-type' : 'application/json',
    'Charset' : 'UTF-8'
}

#print(json.dumps({'instances':temp_values.tolist()}))
resp = requests.post(url = url, 
json = {'instances':temp_values.tolist()}, headers = headers)
print(resp)
print(resp.json())