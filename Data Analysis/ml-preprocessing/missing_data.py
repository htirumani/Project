import datetime
import pandas as pd
import numpy as np
from pprint import pprint

user0 = 'https://raw.githubusercontent.com/htirumani/Project/main/Data%20Analysis/ml-preprocessing/user0_df.csv'
user2 = 'https://raw.githubusercontent.com/htirumani/Project/main/Data%20Analysis/ml-preprocessing/user2_df.csv'

user0r = 'Data Analysis/ml-preprocessing/user0_df.csv'
user2r = 'Data Analysis/ml-preprocessing/user2_df.csv'

def process_heart(df):
    dates = get_dates(df, 'HEART')
  
    for d in dates:
        stime, etime = d
        delta = etime - stime
    if delta.minutes() < 30:
        v = df['HEART'].mean() # update ltr 
        df['HEART'] = df['HEART'].fillna(v)
    else: df.dropna(['HEART'])

# fills in as "asleep" if missing data period is <30 mins and time is not between 0900-2100
def process_sleep(df):
    dates = get_dates(df, 'SLEEP')

    for d in dates:
        stime, etime = d
        delta = etime - stime
    if delta.minutes() < 30 and not ((stime.time.hour > 9) and (etime.time.hour < 21)):
        fill_values(df, 'SLEEP', dates, 0)

    df['SLEEP'] = df['SLEEP'].fillna(0)  

# given steps data has very few null values and no obvious way to fill them, default to fill with 0
def process_steps(df):
    dates = get_dates(df, 'STEPS')
    df['STEPS'] = df['STEPS'].fillna(0)

# get list of tuples (stime, etime) of Nan data in feature
def get_dates(df, feature):
    ixs = df[df[feature].isnull()].index.tolist() # list all null indexes

    # find the start and end indexes of contiguous chunks of indexes
    tups = []
    s = ixs[0]
    p = ixs[0]

    ixs.pop(0)
    for i in ixs:
        if i != p+1: # end of contiguous chunk is reached
            tups.append( (s, p) ) # end of chunk is previous value
            s = i # flag the start of next chunk
            p = i # set i to prev and continue
        else:
            p = i # set i to prev and continue
    tups.append( (s, p) ) # get chunk at end of index list

    date_tups = [(df.at[s, 'DATE'], df.at[e, 'DATE']) for s, e in tups]
    return date_tups


"""
Takes a tuple of dates, and populates feature from start date to end date with value.
"""
def fill_values(df, feature, dates, value):
    sdate, edate = dates
    sindex = pd.Index(df['DATE']).get_loc(str(sdate))
    eindex = pd.Index(df['DATE']).get_loc(str(edate))

    while sindex != eindex:
        df.at[sindex, feature] = value
        sindex += 1


def process_all(fp):
    df = pd.read_csv(fp, index_col=0)
    start_date = df.iloc[0, :1]
    end_date = df.iloc[-1, :1]
    
    process_heart(df)
    process_sleep(df)
    process_steps(df)

    df.dropna(inplace = True)

process_all(user2r)