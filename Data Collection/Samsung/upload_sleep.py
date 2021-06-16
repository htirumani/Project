# This file takes as input a directory of downloaded
# Samsung Health data and extracts minute by minute
# readings, uploads to MongoDB database
import pymongo
import json
import numpy as np
import pandas as pd
import datetime
from pprint import pprint
import os

data_dir_path = '../max-samsung-data'
user_ix = 2
device_ix = 1

print('Collecting Data from Local Files...')

# get unique sleep_stage csv path
csv_path = ''
for d in os.listdir(data_dir_path):
    if 'sleep_stage' in d:
        csv_path = os.path.join(data_dir_path, d)

# read sleep_stage csv file as pandas df
df = pd.read_csv(csv_path, usecols=list(range(11)), skiprows=1)
df = df[['stage', 'start_time', 'end_time']] # filter cols

# convert datetime strings to datetime type
df['start_time'] = pd.to_datetime(df['start_time']) 
df['end_time'] = pd.to_datetime(df['end_time'])

# iterate over rows, then over minutes within time interval
docs = []
delta = datetime.timedelta(minutes=1)
for index, row in df.iterrows():
    start = row['start_time']
    end = row['end_time']

    stage = row['stage']
    stage = 0 if stage == 40001 else 1

    while start != end:
        docs.append({
            'user': user_ix,
            'device': device_ix,
            'datetime': start,
            'stage': stage
        })
        start = start + delta

print('Pushing Data to Database...')

client = pymongo.MongoClient(
    "mongodb+srv://max:iotreu2021@cluster0.bkddq.mongodb.net/wearabledb?retryWrites=true&w=majority",
    ssl=True,
    ssl_cert_reqs='CERT_NONE'
    )
db = client.wearabledb
collection = db.sleep
collection.insert_many(docs)

print('Success')
