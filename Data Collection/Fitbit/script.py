"""
Fetches data off of Fitbit account, adapted from:
https://towardsdatascience.com/using-the-fitbit-web-api-with-python-f29f119621ea

Using an unofficial api from:
https://github.com/orcasgit/python-fitbit
"""

from datetime import datetime
from pymongo import MongoClient
import gather_keys_oauth2 as Oauth2
import fitbit
import json
import os
import sys

# define client id and secret
CLIENT_ID = ''
CLIENT_SECRET = ''

# define MongoDB url
ATLAS = ''

# write file method
def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

# parse body data into appropriate JSON docs
def parse_body(data, user):
    date = data.get()

# parse sleep data into appropriate JSON docs
def parse_sleep(data, user):
    date = data.get('sleep')[0].get('dateOfSleep')
    minData = data.get('sleep')[0].get('minuteData')
    docs = []

    for min in minData: # generate doc using below template
        doc = {
            'user' : user,
            'device' : 0,
            'date' : date,
            'minute' : min.get('dateTime')[:-3],
            'stage' : min.get('value')}
        docs.append(doc)

    return docs

# parse heart rate data into appropriate JSON docs
def parse_heart(data, user):
    date = data.get('activities-heart')[0].get('dateTime')
    minData = data.get('activities-heart-intraday').get('dataset')
    docs = []
    
    for min in minData: # generate doc using below template
        doc = {
            'user' : user,
            'device' : 0,
            'date' : date,
            'minute' : min.get('time')[:-3],
            'heart_rate' : min.get('value')}
        docs.append(doc)

    return docs

# pushes all docs in docs to specified collection in MongoDB
def push_docs(docs, base, feature):
    client = MongoClient(ATLAS)
    db = client[base]
    collection = db[feature]
    collection.insert_many(docs)

# main runner method
def runner(date, user, saveData):
    # authorize API calls
    server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
    server.browser_authorize()
    ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
    REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
    auth2_client = fitbit.Fitbit(CLIENT_ID,CLIENT_SECRET,oauth2=True,access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN)
    day = date

    # get data from API calls
    data_body = auth2_client.body(day)
    data_sleep = auth2_client.sleep(day)
    data_heart = auth2_client.intraday_time_series('activities/heart', day)

    # create relevant docs from API data
    sleep_docs = parse_sleep(data_sleep, user)
    heart_docs = parse_heart(data_heart, user)

    # save data to external JSON files
    if saveData:
        new_dir = os.getcwd() + '/output/' + day
        os.mkdir(new_dir)
        write_json(data_body, new_dir+'/body.json')
        write_json(data_sleep, new_dir+'/sleep.json')
        write_json(data_heart, new_dir+'/heart.json')

    # push docs to MongoDB
    push_docs(sleep_docs, 'test', 'sleep')
    push_docs(heart_docs, 'test', 'heart')

# Verifies arguments
if __name__ == "__main__":
    print(str(sys.argv))
    if len(sys.argv) == 3:
        runner(sys.argv[1], sys.argv[2], False)
    elif len(sys.argv) == 4 and sys.argv[3] == 'y':
        runner(sys.argv[1], sys.argv[2], True)
    else:
        print("Invalid number of arguments, check documentation.")
