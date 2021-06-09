import gather_keys_oauth2 as Oauth2
import fitbit
import pandas as pd 
import datetime
from pymongo import MongoClient
import pymongo
import ssl
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

client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.bkddq.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
print("SSL handshake successful")
db = client['test']
heart = db["heart"]
body = db["body"]
act = db["act"]
sleep = db["sleep"]

for oneDate in allDates:
    
    oneDate = oneDate.date().strftime("%Y-%m-%d")
    data_heart = auth2_client.intraday_time_series('activities/heart', oneDate)
    data_body = auth2_client.body(oneDate)
    data_act = auth2_client.activities(oneDate)
    data_sleep = auth2_client.sleep(oneDate)

    if isinstance(data_heart, list):
        heart.insert_many(data_heart)  
    else:
        heart.insert_one(data_heart) 

    if isinstance(data_body, list):
        body.insert_many(data_body)  
    else:
        body.insert_one(data_body) 


    if isinstance(data_act, list):
        act.insert_many(data_act)  
    else:
        act.insert_one(data_act) 

    if isinstance(data_sleep, list):
        sleep.insert_many(data_sleep)  
    else:
        sleep.insert_one(data_sleep) 

    client.close()

    date_list.append(oneDate)
    
