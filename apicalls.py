import requests
import os
import json

#Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:8000/"

with open('config.json','r') as f:
    config = json.load(f) 

save_data_path = os.path.join(config['output_folder_path']) 

#Call each API endpoint and store the responses
response1 = requests.post(URL + 'prediction')
response2 = requests.get(URL + 'scoring')
response3 = requests.get(URL + 'summarystats')
response4 = requests.get(URL + 'diagnostics')

#combine all API responses
responses = {'prediction': [],
             'scoring': [],
             'summarystats': [],
             'diagnostics': []
             }
responses['prediction'].append(response1.json()['result'])
responses['scoring'].append(response2.json()['result'])
responses['summarystats'].append(response3.json())
responses['diagnostics'].append(response4.json()['result'])
save_path = save_data_path + ('/apireturns.txt')
with open(save_path, 'w') as f:
    for key, value in responses.items(): 
        f.write('%s:%s\n' % (key, value))
#write the responses to your workspace



