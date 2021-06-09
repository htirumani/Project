import gather_keys_oauth2 as Oauth2
import fitbit
import pandas as pd 
import datetime
from pymongo import MongoClient
import json 
import os

# imports various libraries and assigns CLIENT_ID and CLIENT_SECRET to variables.
CLIENT_ID=''
CLIENT_SECRET=''

server=Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN=str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN=str(server.fitbit.client.session.token['refresh_token'])
auth2_client=fitbit.Fitbit(CLIENT_ID,CLIENT_SECRET,oauth2=True,access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN)

startTime = pd.datetime(year = 2021, month = 6, day = 1)
endTime = pd.datetime.today().date() - datetime.timedelta(days=1)
date_list = []
df_list = []
allDates = pd.date_range(start=startTime, end = endTime)

# write file method from Neelam
def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

for oneDate in allDates:
    
    oneDate = oneDate.date().strftime("%Y-%m-%d")
    data_heart = auth2_client.intraday_time_series('activities/heart', base_date=oneDate, detail_level='1sec')
    data_body = auth2_client.body(oneDate)
    data_act = auth2_client.activities(oneDate)
    data_sleep = auth2_client.sleep(oneDate)

    new_dir = os.getcwd() + '/output/' + oneDate
    os.makedirs(new_dir)
    write_json(data_body, new_dir+'/body.json')
    write_json(data_act, new_dir+'/activities.json')
    write_json(data_sleep, new_dir+'/sleep.json')
    write_json(data_heart, new_dir+'/heart.json')
    
    date_list.append(oneDate)
    
