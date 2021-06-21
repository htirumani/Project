# Fetching data from MongoDB
# Aggregating all features to one pandas df
# Look at the data / EDA

# filling in missing values as specified
import datetime
import numpy as np
import pandas as pd
import pymongo
import json
import matplotlib.pyplot as plt
import ssl

# connect to db & grab collections
client = pymongo.MongoClient(
  "mongodb+srv://max:iotreu2021@cluster0.bkddq.mongodb.net/wearabledb?retryWrites=true&w=majority", 
  ssl=True, 
  ssl_cert_reqs='CERT_NONE'
  )
db = client.wearabledb
body = db.body
heart = db.heart
sleep = db.sleep
step = db.step

# define global variables
START_DATE = datetime.datetime(2021, 5, 31)
END_DATE = datetime.datetime(2021, 6, 17)
DELTA = datetime.timedelta(minutes = 1)
USER = 0

# defines various helper methods used in aggregate_feature_cols
def get_user_sleep_data(user):
  print('Collecting Sleep Data...')
  data = []

  docs = sleep.find({'user': user})
  for doc in docs:
    data.append( (doc['datetime'], doc['stage']) )

  return make_df(data, START_DATE, END_DATE)
    
def get_user_hr_data(user):
  print('Collecting Heart Data...')
  data = []

  docs = heart.find({'user': user})
  for doc in docs:
    data.append( (doc['datetime'], doc['heart_rate']) )

  return make_df(data, START_DATE, END_DATE)

def get_user_step_data(user):
  print('Collecting Step Data...')
  data = []

  docs = step.find({'user': user})
  for doc in docs:
    data.append( (doc['datetime'], doc['steps']) )

  return make_df(data, START_DATE, END_DATE)

def get_user_body_data(user):
  print('Collecting Body Data...')
  height = []
  weight = []

  docs = body.find({'user': user})
  for doc in docs:
    height.append( (doc['datetime'], doc['height']) )
    weight.append( (doc['datetime'], doc['weight']) )

  return (
    make_df(height, START_DATE, END_DATE),
    make_df(weight, START_DATE, END_DATE)
  )

def make_df(data, sdate, edate):
  vdates = [x[0] for x in data]
  
  col = []
  while sdate != edate:
    if sdate in vdates:
      x = [x[1] for x in data if x[0] == sdate][0]
      col.append(x)
    else:
      col.append(None)
    
    sdate += DELTA
  
  return col

def aggregate_feature_cols(user):
  sleep_df = get_user_sleep_data(user)
  heart_df = get_user_hr_data(user)
  step_df = get_user_step_data(user)
  weight_df, height_df = get_user_body_data(user)


  print('Aggregating...')
  sdate = START_DATE
  edate = END_DATE

  date_df = []
  user_df = []
  while sdate != edate:
    date_df.append(sdate)
    user_df.append(user)

    sdate += DELTA

  return pd.DataFrame({
    'DATE': date_df, 
    'USER': user_df,
    'SLEEP': sleep_df,
    'HEART': heart_df,
    'STEP': step_df,
    'WEIGHT': weight_df,
    'HEIGHT': height_df
    })

df = aggregate_feature_cols(USER)
df.to_csv('user{}_df.csv'.format(USER))
print('done')