
import pandas as pd
import numpy as np
import timeit
import os
import json
import pickle
import subprocess
from ingestion import merge_multiple_dataframe
from training import train_model

##################Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path']) 
model_path = os.path.join(config['output_model_path']) 

##################Function to get model predictions
def model_predictions(data):
    #read the deployed model and a test dataset, calculate predictions
    with open(model_path + "/" + 'trainedmodel.pkl', 'rb') as file:
        model = pickle.load(file)
    X = data[['lastmonth_activity','lastyear_activity','number_of_employees']].values.reshape(-1, 3)
    predicted = model.predict(X).tolist()
    return predicted

##################Function to get summary statistics
def dataframe_summary():
    #calculate summary statistics here
    data_df = pd.read_csv(dataset_csv_path + "/" + 'finaldata.csv')
    result = {'mean':[],
              'median':[],
              'std':[]}
    result['mean'].append(data_df.mean())
    result['median'].append(data_df.median())
    result['std'].append(data_df.std())

    return result

##################Function to get timings
def execution_time():
    #calculate timing of training.py and ingestion.py
    starttime = timeit.default_timer()
    merge_multiple_dataframe()
    ingestion_timing=timeit.default_timer() - starttime

    starttime = timeit.default_timer()
    train_model()
    training_timing=timeit.default_timer() - starttime
    return(ingestion_timing, training_timing)

##################Function to check dependencies
def outdated_packages_list():
    #get a list of 
    outdated = subprocess.check_output(['pip', 'list','--outdated'])
    with open('outdated.txt', 'wb') as f:
        f.write(outdated)
    return 'outdated.txt updated'


if __name__ == '__main__':
    data=pd.read_csv(test_data_path + "/" + 'testdata.csv')
    print(model_predictions(data))
    print(dataframe_summary())
    execution_time()
    outdated_packages_list()





    
