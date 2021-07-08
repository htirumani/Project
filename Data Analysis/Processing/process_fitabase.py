import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from pprint import pprint

from process import process_heart, process_sleep, process_steps, add_null, add_null_improved, add_null_pd

path = '../Fitabase-Data-All'

'''
Converts 15 second resolution heart rate dataframe to 1 minute resolution and keeps only observations where user
is in 'users'. Saves reduced dataframe to path if it hasn't already been saved.
'''
def reduce_heart_df(heart_df, fp):
    print('Reducing...')
    # eventual columns
    date = []
    user = []
    heart = []

    # looping variables
    pmin = None
    puser = None
    vals = []
    for _, row in heart_df.iterrows():
        # first iteration
        if pmin == None:
            pmin = pd.to_datetime(row['Time']).replace(second=0)
        
        cmin = pd.to_datetime(row['Time']).replace(second=0)
        if pmin != cmin:
            date.append(pmin)
            user.append(puser)
            heart.append(int(np.mean(vals)))
            vals = []
            
        pmin = cmin
        puser = row['Id']
        vals.append(row['Value'])
    
    # last iteration
    date.append(pmin)
    user.append(puser)
    heart.append(int(np.mean(vals)))

    df = pd.DataFrame({'USER': user, 'DATE': date, 'HEART': heart})
    if not os.path.exists(fp):
        df.to_csv(fp)

    return df

'''
Sleep data is sometimes reported at time XX:XX:30, needs to be at XX:XX:00
'''
def correct_sleep_df(sleep_df):
    times = sleep_df['date'].tolist()
    times = [t.replace(second = 0) for t in times]
    sleep_df['date'] = times

'''
Returns a list of users for which data exists in sleep, heart, and step files.
'''
def get_common_users(sleep_df, heart_df, step_df):
    sleep_list = sleep_df['Id'].unique().tolist()
    heart_list = heart_df['USER'].unique().tolist()
    step_list = step_df['Id'].unique().tolist()

    common_users = list(set(sleep_list) & set(heart_list) & set(step_list))
    return common_users

'''
Given a user, returns a tuple of the earliest and latest records in the SLEEP csv file.
'''
def get_user_date_range(sleep_df, user_id):
    df = sleep_df[sleep_df['Id'] == user_id]
    dates = (df['date'].min(), df['date'].max())

    return dates

def get_minutes_list(stime, etime):
    delta = timedelta(minutes=1)
    times = []
    while stime != etime:
        times.append(stime.to_datetime64())
        stime = stime + delta
    
    return times


def process_all(root_path, processed_heart_fp):
    sleep_path = root_path + '/minuteSleep_merged_all.csv'
    heart_path = root_path + '/heartrate_seconds_merged_all.csv'
    step_path = root_path + '/minuteStepsNarrow_merged_all.csv'

    print('Constructing Sleep DF')
    sleep_df = pd.read_csv(sleep_path, parse_dates=['date'])
    correct_sleep_df(sleep_df)

    heart_df = None
    if processed_heart_fp != None and os.path.exists(processed_heart_fp):
        print('Getting saved preprocessed HR df')
        heart_df = pd.read_csv(processed_heart_fp, parse_dates=['DATE'])
    else:
        print('Constructing and Reducing HR df')
        heart_df = pd.read_csv(heart_path)
        heart_df = reduce_heart_df(heart_df, processed_heart_fp)

    print('Constructing Step DF')
    step_df = pd.read_csv(step_path, parse_dates=['ActivityMinute'])

    print('Getting users')
    users = get_common_users(sleep_df, heart_df, step_df)

    print('Getting date ranges')
    ranges = [(user, get_user_date_range(sleep_df, user)) for user in users]

    delta = timedelta(minutes=1)
    for user, (stime, etime) in ranges:

        print('Processing user: {}'.format(user))

        print('Setting up...')
        times = get_minutes_list(stime, etime)

        sleep = [None for i in range(len(times))]
        heart = [None for i in range(len(times))]
        step = [None for i in range(len(times))]

        print('Subsetting...')
        user_sleep = sleep_df[sleep_df['Id'] == user]
        user_heart = heart_df[heart_df['USER'] == user]
        user_step = step_df[step_df['Id'] == user]

        date_list = get_minutes_list(stime, etime)

        print('Processing Sleep...')
        sleep_dates = user_sleep['date'].tolist()
        sleep_values = user_sleep['value'].tolist()
        sleep_list = [(d, 1) for d, v in zip(sleep_dates, sleep_values) if v != 3]  # omitted v=3 values will be repopulated with 'awake' on cleaning
        print('...')
        sleep_list = add_null_improved(sleep_list, stime, etime)
        
        print('Processing Heart...')
        heart_dates = user_heart['DATE'].tolist()
        heart_values = user_heart['HEART'].tolist()
        heart_list = [(d, v) for d, v in zip(heart_dates, heart_values)]
        print('...')
        heart_list = add_null_improved(heart_list, stime, etime)

        print('Processing Step...')
        step_dates = user_step['ActivityMinute'].tolist()
        step_values = user_step['Steps'].tolist()
        step_list = [(d, v) for d, v in zip(step_dates, step_values)]
        print('...')
        step_list = add_null_improved(step_list, stime, etime)

        print('Cleaning...')
        df = pd.DataFrame({
            'DATE': date_list,
            'USER': user,
            'SLEEP': sleep_list,
            'HEART': heart_list,
            'STEP': step_list})

        df.to_csv('user{}_raw.csv'.format(user))

        process_heart(df)
        process_sleep(df)
        process_steps(df)
        df.dropna(inplace=True)
        df['USER'] = df['USER'].astype(int)
        df['HEART'] = df['HEART'].astype(int)
        df['SLEEP'] = df['SLEEP'].astype(int)
        df['STEP'] = df['STEP'].astype(int)

        df.to_csv('user{}_clean.csv'.format(user))

process_all(path, path + '/minuteHR_reduced_all.csv')

