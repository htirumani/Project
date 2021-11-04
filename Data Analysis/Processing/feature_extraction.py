from datetime import datetime, date, time
from datetime import timedelta
import pandas as pd
import numpy as np
from pprint import pprint
from matplotlib import pyplot as plt
import os

from process import add_null_improved

'''
Given a clean dataframe FROM A SINGLE USER, returns a list of tuples
containing start and end times of contiguous chunks of data.
'''
def get_contiguous_chunks(df):
    # get data sorted by date
    sdf = df.sort_values('DATE', ascending=True)
    ixs = np.array(list(range(sdf.shape[0])))
    sdf.set_index(ixs, inplace = True)

    tups = []
    s = sdf.at[0, 'DATE']
    p = sdf.at[0, 'DATE']
    l = 0
    delta = timedelta(minutes = 1)
    for index, row in sdf.iterrows():
        if index == 0: continue

        c = row['DATE']
        if c != p+delta:
            tups.append( (s, p, l) )
            s = c
            l = 0
        else:
            l += 1
        p = c
    tups.append( (s, p, l) )

    return tups

'''
0 for 9am-9pm, 1 else
'''
def append_nighttime_feature(df):
    times = df['DATE'].to_list()
    hours = [int(t.hour < 9 or t.hour > 21) for t in times]

    df['NIGHTTIME'] = hours

'''
1 for Monday - Friday, 0 for Saturday - Sunday
'''
def append_weekday_feature(df):
    times = df['DATE'].to_list()
    days = []
    for time in times:
        time = time[:-9]
        if datetime.datetime.strptime(time, '%Y-%m-%d').weekday():
            days.append(1)
        else: days.append(0)
    modded = df.assign(WEEKDAY=days)
    df = modded

'''
Helper for append_activity_feature
'''
def get_cutoff(dt):
    if dt.time().hour < 4:
        return dt.replace(hour=4, minute=0)
    else:
        return (dt + timedelta(days = 1)).replace(hour = 4, minute = 0)

'''
minute-by-minute running total of steps that turns over at 4am
'''
def append_activity_feature(df):
    steps = df['STEP'].to_list()
    times = df['DATE'].to_list()
    activity = []

    sum = 0
    cutoff = get_cutoff(times[0])
    for step, time in zip(steps, times):

        if time > cutoff:
            sum = 0
            cutoff = get_cutoff(time)
        else: 
            sum += step
        
        activity.append(sum)

    df['ACTIVITY'] = activity

'''
how many minutes of sleep in the past 24 hrs
'''
def append_previous_sleep_feature(df):
    sleep = df['SLEEP'].tolist()
    mins_of_sleep = 0
    minutes_since_reset = 0
    previous_sleep = []
    for s in sleep:
        if (minutes_since_reset > 1440):
            minutes_since_reset = 0
            mins_of_sleep = 0
        elif (s == 1):
            mins_of_sleep += 1
        minutes_since_reset += 1
        previous_sleep.append(mins_of_sleep)
    df['PSLEEP'] = previous_sleep

'''
Sum of minutes labeled asleep in the previous 'window' HOURS
'''
def append_historical_sleep_feature(df, window):
    sleep = df['SLEEP'].tolist()
    times = df['DATE'].tolist()
    data = [(t, s) for t, s in zip(times, sleep)]

    sleep = add_null_improved(data, times[0], times[-1])

    mins = window * 60
    stotal = []
    for i, s in enumerate(sleep):
        rmin = max(0, i - mins)
        stotal.append(sum(filter(None, sleep[rmin:i+1])))

    stotal = [total for total, s in zip(stotal, sleep) if s != None]
    stotal.append(0) ########### FIXME
    label = '{}HR_SLEEP_TOTAL'.format(window)
    df[label] = stotal

'''
at each minute, gives the sum of the minutes recorded as asleep in the previous n hours.
'''
def append_n_hour_sleep_total(n):
    pass

'''
appends both MEAN_{}MIN_HR and SD_{}MIN_HR
corresponding to mean and sd of HR data for previous 'window' minutes

note: requires the omittion of rows without 'window' minutes of data
immediately preceding them
'''
def append_historical_hr_features(df, window):
    mean_label = 'MEAN_{}MIN_HR'.format(window)
    sd_label = 'SD_{}MIN_HR'.format(window)
    
    df.sort_values('DATE', ascending=True, inplace=True)
    ixs = np.array(list(range(df.shape[0])))
    df.set_index(ixs, inplace = True)

    df[mean_label] = None
    df[sd_label] = None

    for index, row in df.iterrows():
        
        # attempt to get row's preceding HR values
        hist = []
        punt = False
        for m in range(1, window+1):
            if punt: break

            if index - m < 0: 
                punt = True
                continue

            curr = df.at[index-m, 'DATE']
            if curr != row['DATE'] - timedelta(minutes=m): 
                punt = True
                continue

            hist.append(df.at[index-m, 'HEART'])
        
        # append mean and sd of hist if all data is collected
        if not punt:
            df.at[index, mean_label] = np.mean(hist)
            df.at[index, sd_label] = np.std(hist)
        
    df.dropna(inplace=True)

'''
Appends the sum of the previous 'window' minutes of steps to each row.

Rows missing from the immediate history are assumed 0 values.
'''
def append_historical_step_feature(df, window):
    label = '{}MIN_STEP_SUM'.format(window)
    
    df['DATE'] = pd.to_datetime(df['DATE'])
    df.sort_values('DATE', ascending=True, inplace=True)
    ixs = np.array(list(range(df.shape[0])))
    df.set_index(ixs, inplace = True)

    df[label] = None

    for index, row in df.iterrows():
        # attempt to get row's preceding Step values
        hist = []
        for m in range(1, window+1):
            if index - m < 0: 
                continue

            curr = df.at[index-m, 'DATE']
            if curr != row['DATE'] - timedelta(minutes=m): 
                continue

            hist.append(df.at[index-m, 'STEP'])
        
        # append sum of hist if all data is collected
        df.at[index, label] = np.sum(hist)
        
    df.dropna(inplace=True)

'''
Appends a column to the dataframe representing the number of minutes from midnight of the current time
'''
def append_min_midnight(df):
  d = date.today()
  m = datetime.combine(d, time(0))
  times = df['DATE'].to_list()
  min = [int((datetime.combine(d, t.time())-m).total_seconds() / 60)
        for t in times]
  df['MINFROMMIDNIGHT'] = min

'''
Binary variable indicating the probability the user will be asleep in the next n minutes.
'''
def append_nmin_sleep_prob(df, n):
    sleep = df['SLEEP'].tolist()
    dates = df['DATE'].tolist()
    probs = [None for i in sleep]

    for i, (s, d) in enumerate(zip(sleep, dates)):
        if s != 1:
            probs[i] = 0
            continue

        probs[i] = None
        for diff in range(1, n + 1):
            j = i - diff
            if j < 0: break                                 # break if index is bad
            if ((d - dates[j]).seconds / 60) < n: continue   # break if preceding index doesn't represent preceding time
            if sleep[j] == 1: continue                         # break if user is asleep at index
            probs[j] = 1  # assign future sleep probability to 1
    
    label = '{}MIN_SLEEP_PROB'.format(n)
    df[label] = probs

'''
Takes a list of filepaths, appends extracted features from the data in those files, saves new data to files in 'final' folder.

fps: list of data files on which to append features
users: list of user indexes corresponding to files in fps
combine_filename: if not none, appends all user's processed data to a file 'combined_filename'
validation: should the processed files go into the validation folder
sleep_prob: append sleep probability variable?
sleep_prob_n: integer or list of integers specifying the 'n' value for sleep probability, if list append a column for each n value.
nighttime... : boolean on whether to include said feature
'''
def append_and_write(fps, users, combine_filename=None, validation=False,
            sleep_prob=False,
            sleep_prob_n=None,
            nighttime=False,
            historical_hr=False,
            historical_hr_window=None,
            activity=False,
            historical_step=False,
            historical_step_window=None,
            previous_sleep=False,
            weekday=False,
            mins_to_midnight=False,
            historical_sleep=True,
            historical_sleep_windows=None,
            **kwargs
            ):
    all_dfs = []
    for path, user in zip(fps, users):
        print('Processing user', user)
        df = pd.read_csv(path, parse_dates=['DATE'])

        if nighttime:
            print('Appending nighttime...')
            append_nighttime_feature(df)
        if historical_hr:
            print('Appending historical HR...')
            append_historical_hr_features(df, historical_hr_window)
        if activity:
            print('Appending Activity...')
            append_activity_feature(df)
        if historical_step:
            print('Appending Historical Step...')
            append_historical_step_feature(df, historical_step_window)
        if previous_sleep:
            print('Appending Previous Sleep...')
            append_previous_sleep_feature(df)
        if weekday:
            print('Appending Weekday...')
            append_weekday_feature(df)
        if mins_to_midnight:
            print('Appending Minutes to Midnight....')
            append_min_midnight(df)
        if historical_sleep:
            for i in historical_sleep_windows:
                print('Appending {}HR Historical Sleep...'.format(i))
                append_historical_sleep_feature(df, i)

        if sleep_prob:
            if type(sleep_prob_n) != list:
                print('Appending {}min sleep prob...'.format(sleep_prob_n))
                append_nmin_sleep_prob(df, sleep_prob_n)
            else:
                for n in sleep_prob_n:
                    print('Appending {}min sleep prob...'.format(n))
                    append_nmin_sleep_prob(df, n)

        print('Writing data...')
        if validation:
            df.to_csv('Data Analysis/Dataset/final/validation/user{}_featured.csv'.format(user))
        else:
            df.to_csv('Data Analysis/Dataset/final/user{}_featured.csv'.format(user))

        if combine_filename != None: all_dfs.append(df)
    
    if combine_filename != None:
        all_df = pd.concat(all_dfs)
        all_df.to_csv('Data Analysis/Dataset/final/combined/' + combine_filename)

    print('Done')

def main():
    data_path = 'Data Analysis/Dataset/clean/'
    fps = os.listdir(data_path)
    fps.remove('all_clean.csv')
    users = [int(u[4:-10]) for u in fps] # extract integer id from filename

    val_fps = ['user4020332650_clean.csv', 'user6775888955_clean.csv']
    val_users = [int(u[4:-10]) for u in val_fps]

    for fp in val_fps: fps.remove(fp)
    for u in val_users: users.remove(u)

    fps = [data_path + fp for fp in fps]
    val_fps = [data_path + fp for fp in val_fps]

    feature_args = {
        'sleep_prob': True,
        'sleep_prob_n': [5, 15, 30, 60],
        'nighttime': False,
        'historical_hr': False,
        'historical_hr_window': None,
        'activity': True,
        'historical_step': True,
        'historical_step_window': 10,
        'previous_sleep': True,
        'weekday': False,
        'mins_to_midnight': True,
        'historical_sleep': True,
        'historical_sleep_windows': [8, 12, 24]
    }

    # Append features for train/test set
    append_and_write(fps, users, combine_filename='all_featured.csv', **feature_args)

    # Append features for validation set
    append_and_write(val_fps, val_users, combine_filename='validation_featured.csv', validation=True, **feature_args)

if __name__ == '__main__':
    main()
