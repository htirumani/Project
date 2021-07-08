'''
script takes a directory of desired files from 'Fitabase-Data-All' directory, combines
the separate files from each feature, sorts them by Id then date, and returns a merged file.
'''
import pandas as pd
import os

path = '../Fitabase-Data-All'

labels = ['/heartrate_seconds_merged', '/minuteSleep_merged', '/minuteStepsNarrow_merged']
tlabels = ['Time', 'date', 'ActivityMinute']

for label, tlabel in zip(labels, tlabels):
    print('processing {}...'.format(label))
    df0 = pd.read_csv(path + label + '_0' + '.csv', parse_dates=[tlabel])
    df1 = pd.read_csv(path + label + '_1' + '.csv', parse_dates=[tlabel])

    df = pd.concat([df0, df1])
    df.reset_index(inplace=True)
    df.drop('index', axis=1, inplace=True)
    df.drop_duplicates(inplace=True)
    df.sort_values(['Id', tlabel], inplace=True)

    df.to_csv(path + label + '_all.csv')

print('done')