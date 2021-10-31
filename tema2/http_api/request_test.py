import requests
import json


header = {'Content-Type': 'application/json'}
data = {'subnet': '10.189.24.0/24', 'dim': [10, 10, 100]}
url = 'http://ec2-3-86-219-129.compute-1.amazonaws.com/subnet' # link-ul catre serverul AWS
response = requests.post(url, headers=header, data=json.dumps(data))
print(response.content)