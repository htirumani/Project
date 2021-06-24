from datetime import datetime
import pandas as pd
import numpy as np
from pprint import pprint
from matplotlib import pyplot as plt

path = 'Data Analysis/processed-data-files/all_df_clean.csv'
df = pd.read_csv(path, index_col=0, parse_dates=['DATE'])

'''
0 for 9am-9pm, 1 else
'''
def append_nighttime_feature(df):
    times = df['DATE'].to_list()
    hours = [int(t.hour < 9 or t.hour > 21) for t in times]

    df['NIGHTTIME'] = hours

'''
appends both MEAN_{}MIN_HR and SD_{}MIN_HR
corresponding to mean and sd of HR data for previous 'window' minutes
'''
def append_historical_hr_features(window):
    pass