from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json



#################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

model_path = os.path.join(config['output_model_path']) 
test_data_path = os.path.join(config['test_data_path']) 


#################Function for model scoring
def score_model(data = pd.read_csv(test_data_path + "/" + 'testdata.csv')):
    #this function should take a trained model, load test data, and calculate an F1 score for the model relative to the test data
    with open(model_path + "/" + 'trainedmodel.pkl', 'rb') as file:
        model = pickle.load(file)

    # if data == None:
    #     data=pd.read_csv(test_data_path + "/" + 'testdata.csv')

    X = data[['lastmonth_activity','lastyear_activity','number_of_employees']].values.reshape(-1, 3)
    y = data['exited'].values.reshape(-1,1)

    predicted = model.predict(X)

    f1score = metrics.f1_score(predicted,y)
    #it should write the result to the latestscore.txt file
    f = open("./" + model_path + "/" + "latestscore.txt", "w")
    f.write(str(f1score))
    f.close()
    return f1score

if __name__ == '__main__':
    score_model()

