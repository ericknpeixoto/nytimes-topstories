#%%

import json
import requests
import dotenv
import os

#%%

# Setup enviroment varibles for databricks authetication
dotenv.load_dotenv('.env')
db_token = os.getenv('DATABRICKS_TOKEN')
db_host = os.getenv('DATABRICKS_HOST')
db_jobid = os.getenv('DATABRICKS_JOBID')
db_user = os.getenv('DATABRICKS_USER')



#%%

# Load the file with the new settings for the Databricks Workflow
def load_settings(job_name):

  with open(f'{job_name}.json', 'r') as settings_file:
    new_settings = json.load(settings_file)
    new_settings['job_id'] = int(db_jobid)
    new_settings['new_settings']['run_as']['user_name'] = db_user

    for task in new_settings['new_settings']['tasks']:
      task['email_notifications']['on_success'] = [db_user]
      task['email_notifications']['on_failure'] = [db_user]
    return new_settings

#%%

# Updates the workflow settings in Databricks
def update_settings(url, headers, new_settings):
  return requests.post(url, headers=headers, json=new_settings)

# %%

# Runs the code

url = f'{db_host}/api/2.2/jobs/reset?job_id={db_jobid}'
headers = {"Authorization": f"Bearer {db_token}"}
new_settings = load_settings('nytimes')

resp = update_settings(url, headers, new_settings)

if resp == 200:
  print('Databricks job update successfully')
else: 
  print('Error uploading the job: ', resp.content)

  

 


