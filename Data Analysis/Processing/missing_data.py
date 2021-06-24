from datetime import datetime
import pandas as pd
import numpy as np
from pprint import pprint
from matplotlib import pyplot as plt

user0 = 'https://raw.githubusercontent.com/htirumani/Project/main/Data%20Analysis/ml-preprocessing/user0_df.csv'
user2 = 'https://raw.githubusercontent.com/htirumani/Project/main/Data%20Analysis/ml-preprocessing/user2_df.csv'

user0r = 'Data Analysis/processed-data-files/user0_df.csv'
user1r = 'Data Analysis/processed-data-files/user1_df.csv'
user2r = 'Data Analysis/processed-data-files/user2_df.csv'

'''
Help from https://stackoverflow.com/questions/2119472/convert-a-timedelta-to-days-hours-and-minutes
'''
def process_heart(df):
    dates = get_dates(df, 'HEART')
  
    for d in dates:
        stime, etime = d
        stime, etime = datetime.strptime(stime, '%Y-%m-%d %H:%M:%S'), datetime.strptime(etime, '%Y-%m-%d %H:%M:%S')
        delta = etime - stime
        days, hours, minutes = delta.days, delta.seconds // 3600, delta.seconds // 60 % 60
        if minutes < 30:
            v = mean_surrounding_values(df, 'HEART', d)
            fill_values(df, 'HEART', d, v)
        
    df.dropna(subset=['HEART'], inplace=True)

# fills in as "asleep" if missing data period is <30 mins and time is not between 0900-2100
def process_sleep(df):
    dates = get_dates(df, 'SLEEP')

    for d in dates:
        stime, etime = d
        stime, etime = datetime.strptime(stime, '%Y-%m-%d %H:%M:%S'), datetime.strptime(etime, '%Y-%m-%d %H:%M:%S')
        delta = etime - stime
        days, hours, minutes = delta.days, delta.seconds // 3600, delta.seconds // 60 % 60
        if minutes < 30 and not ((stime.time().hour > 9) and (etime.time().hour < 21)):
            fill_values(df, 'SLEEP', d, 0)

    df['SLEEP'] = df['SLEEP'].fillna(0)

# given steps data has very few null values and no obvious way to fill them, default to fill with 0
def process_steps(df):
    df['STEP'] = df['STEP'].fillna(0)

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

def mean_surrounding_values(df, feature, dates):
    sdate, edate = dates
    sindex = pd.Index(df['DATE']).get_loc(str(sdate))
    eindex = pd.Index(df['DATE']).get_loc(str(edate))

    if sindex == 0:
        return df.at[eindex + 1, feature]

    if eindex == df.shape[0] - 1:
        return df.at[sindex - 1, feature]

    before = df.at[sindex - 1, feature]
    after = df.at[eindex + 1, feature]

    m = int(np.mean([before, after]).item())

    return m


def process_all(fp):
    df = pd.read_csv(fp, index_col=0)
    start_date = df.iloc[0, :1]
    end_date = df.iloc[-1, :1]
    
    # process missing values IN THIS ORDER
    process_heart(df)
    process_sleep(df)
    process_steps(df)

    df.dropna(inplace=True)  # drop remaining missing values
    
    df['USER'] = df['USER'].astype(int)
    df['SLEEP'] = df['SLEEP'].astype(int)
    df['HEART'] = df['HEART'].astype(int)
    df['STEP'] = df['STEP'].astype(int)
    df['WEIGHT'] = df['WEIGHT'].astype(int)
    df['HEIGHT'] = df['HEIGHT'].astype(int)

    return df

# df0 = process_all(user0r)
df1 = process_all(user1r)
# df2 = process_all(user2r)
# merged = pd.concat([df0, df2])

# print('NUM ROWS')
# print('Neelam:', df0.shape[0])
# print('Max:', df2.shape[0])
# print('All:', merged.shape[0])

# print('\nNEELAM')
# print(df0.describe())

# print('\nMAX')
# print(df2.describe())

# print('\nALL')
# print(merged.describe())

# df0.to_csv('user0_df_clean.csv')
df1.to_csv('user1_df_clean.csv')
# df2.to_csv('user2_df_clean.csv')
# merged.to_csv('all_df_clean.csv')
