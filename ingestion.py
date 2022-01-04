import pandas as pd
import numpy as np
import os
import json
from datetime import datetime




#############Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']



#############Function for data ingestion
def merge_multiple_dataframe():
    #check for datasets, compile them together, and write to an output file
    filenlist = os.listdir(os.getcwd()+"/"+input_folder_path)
    data_df = pd.DataFrame()
    for file in filenlist:
        # print("./" + input_folder_path + "/" + file)
        currentdf = pd.read_csv("./" + input_folder_path + "/" + file)
        data_df = data_df.append(currentdf)
    data_df.to_csv("finaldata.csv")
    f = open("./" + output_folder_path + "/" + "ingestedfiles.txt", "a")
    f.write(str(filenlist))
    f.close()

if __name__ == '__main__':
    merge_multiple_dataframe()
