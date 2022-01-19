import pickle
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from diagnostics import model_predictions



###############Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_model_path']) 
test_data_path = os.path.join(config['test_data_path']) 




##############Function for reporting
def score_model():
    #calculate a confusion matrix using the test data and the deployed model
    testdata=pd.read_csv(test_data_path + "/" + 'testdata.csv')
    y_true = testdata['exited'].values.reshape(-1,1)
    predict = model_predictions(testdata)
    matrix = confusion_matrix(y_true, predict)
    #write the confusion matrix to the workspace
    sns.heatmap(matrix, annot=True)
    plt.savefig(dataset_csv_path + "/" + 'confusionmatrix.png')





if __name__ == '__main__':
    score_model()
