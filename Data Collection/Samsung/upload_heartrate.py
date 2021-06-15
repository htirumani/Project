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

# get unique heartrate csv path
heartrate_csv_path = ''
for d in os.listdir(data_dir_path):
    if 'heart_rate' in d:
        heartrate_csv_path = os.path.join(data_dir_path, d)

# read heartrate csv file as pandas df
hr_csv = pd.read_csv(heartrate_csv_path, usecols=list(range(15)), skiprows=1)
hr_csv = hr_csv[['binning_data', 'start_time', 'end_time']] # filter cols
hr_csv = hr_csv[hr_csv.binning_data.notnull()] # keep only rows with min-to-min data

hr_csv['start_time'] = pd.to_datetime(hr_csv['start_time']) # convert datetime strings to datetime type
hr_csv['end_time'] = pd.to_datetime(hr_csv['end_time'])

# iterate over rows to find bins
docs = []
for index, row in hr_csv.iterrows():
    dt = row['start_time']
    delta = datetime.timedelta(minutes=1)

    # get binning data file
    bin_key = row['binning_data'] + '.json'
    bin_path = os.path.join(data_dir_path, 'jsons', 'com.samsung.health.heart_rate', bin_key)

    # check that bin file exists
    if not os.path.exists(bin_path):
        print('No such file', bin_path)
        continue

    # convert bin json to python dictionary
    raw_minute_data = 0
    with open(bin_path) as json_file:
        raw_minute_data = json.load(json_file)

    # create formatted python dictionary
    for i in raw_minute_data:
        docs.append({
            'user': user_ix,
            'device': device_ix,
            'date': dt.strftime('%Y-%m-%d'),
            'minute': dt.strftime('%H:%M'),
            'heart_rate': int(i['heart_rate'])
        })
        dt = dt + delta

print('Pushing Data to Database...')

client = pymongo.MongoClient("mongodb+srv://max:iotreu2021@cluster0.bkddq.mongodb.net/test?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
db = client.test
collection = db.heart
collection.insert_many(docs)

print('Success')
