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


def get_combined_device_id(root_dir):
    # get unique step_count csv path
    csv_path = ''
    for d in os.listdir(root_dir):
        if 'device_profile' in d:
            csv_path = os.path.join(root_dir, d)

    data = pd.read_csv(csv_path, usecols=list(range(16)), skiprows=1)
    return data[data['name'] == 'Combined']['deviceuuid'].item()

data_dir_path = '../max-samsung-data'
device_id = get_combined_device_id(data_dir_path)
user_ix = 2
device_ix = 1

print('Collecting Data from Local Files...')

# get unique pedometer_day_summary csv path
csv_path = ''
for d in os.listdir(data_dir_path):
    if 'pedometer_day_summary' in d:
        csv_path = os.path.join(data_dir_path, d)

# read pedometer csv file as pandas df
df = pd.read_csv(csv_path, usecols=list(range(19)), skiprows=1 )
df = df[['binning_data', 'create_time', 'deviceuuid']] # filter cols

# convert datetime strings to datetime type
df['create_time'] = pd.to_datetime(df['create_time'])

# take only watch measurements, sort by date for iteration
df = df[df['deviceuuid'] == device_id]
df = df.sort_values(by='create_time', ignore_index=True)

# iterate over rows to find bins
docs = []
for index, row in df.iterrows():
    dt = row['create_time']

    # get binning data file
    bin_key = row['binning_data'] + '.json'
    bin_path = os.path.join(data_dir_path, 'jsons', 'com.samsung.shealth.tracker.pedometer_day_summary', bin_key)

    # check that bin file exists
    if not os.path.exists(bin_path):
        print('No such file', bin_path)
        continue

    # convert bin json to python dictionary
    raw_data = 0
    with open(bin_path) as json_file:
        raw_data = json.load(json_file)

    # create formatted python dictionary
    active_time = datetime.datetime(dt.year, dt.month, dt.day, 0, 0)
    one_min = datetime.timedelta(minutes=1)
    running_total = 0
    for i in raw_data:
        running_total += i['mStepCount']
        for j in range(10):
            docs.append({
                'user': user_ix,
                'device': device_ix,
                'date': dt.strftime('%Y-%m-%d'),
                'minute': active_time.strftime('%H:%M'),
                'steps': running_total
            })
            active_time = active_time + one_min

with open('steps.json', 'w') as outfile:
    json.dump(docs, outfile)

print('Pushing Data to Database...')

client = pymongo.MongoClient("mongodb+srv://max:iotreu2021@cluster0.bkddq.mongodb.net/test?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
db = client.test
collection = db.step
collection.insert_many(docs)

print('Success')