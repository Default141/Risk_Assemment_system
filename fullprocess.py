import json
import os
import pandas as pd
import ingestion
import training
import scoring
import deployment
import apicalls
import reporting


##################Check and read new data
#first, read ingestedfiles.txt
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']
prod_folder_path = config['prod_deployment_path']

filenlist = os.listdir(os.getcwd()+"/"+input_folder_path)
#second, determine whether the source data folder has files that aren't listed in ingestedfiles.txt
filenlist_orgin = open("./" + output_folder_path + "/" + "ingestedfiles.txt", "r")
file = filenlist_orgin.read()
file_origin_list  = file.split(',')

##################Deciding whether to proceed, part 1
#if you found new data, you should proceed. otherwise, do end the process here
if(set(file_origin_list) != set(filenlist)):
    ingestion.merge_multiple_dataframe()
    ##################Checking for model drift
    #check whether the score from the deployed model is different from the score from the model that uses the newest ingested data
    latestscore = open("./" + prod_folder_path + "/" + "latestscore.txt", "r").read()
    print(latestscore)
    new_score = scoring.score_model(pd.read_csv(output_folder_path + "/" + 'finaldata.csv'))
    print(new_score)
    ##################Deciding whether to proceed, part 2
    #if you found model drift, you should proceed. otherwise, do end the process here
    if new_score < float(latestscore):
        ##################Re-deployment
        #if you found evidence for model drift, re-run the deployment.py script
        training.train_model()
        deployment.store_model_into_pickle()

    else:
        print('not drift')
else:
    print('end')

apicalls.call_api()
reporting.score_model()










##################Diagnostics and reporting
#run diagnostics.py and reporting.py for the re-deployed model







