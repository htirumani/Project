# plot where y axis is feature and x is time.
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

import matplotlib as mpl
mpl.rc('image', cmap='bwr')

ddir = 'preds'
l = os.listdir(ddir)

# l.remove('combined')
# l.remove('validation')

# l.remove('all_clean.csv')

# l = ['user2347167796_featured.csv']
# l = l[0:1]

for i in l:
    print(i)
    df = pd.read_csv(ddir + '/' + i, parse_dates=['DATE'])
    d = df['DATE']
    heart = df['HEART']
    sleep = df['SLEEP'] * 16000
    step = df['STEP']
    activity = df['ACTIVITY']
    step10min = df['10MIN_STEP_SUM']
    midnight = df['MINFROMMIDNIGHT']
    HR10min_mean = df['MEAN_10MIN_HR']
    HR10min_sd = df['SD_10MIN_HR']
    correct = df['CORRECT']
    incorrect = (-correct) + 1

    plt.figure(figsize=(25,12))
    plt.stem(d, sleep, markerfmt=' ', linefmt='lightgray', basefmt='white')
    plt.scatter(d, activity, c=incorrect, s=5, zorder=2, alpha=0.5, linewidth=0.5)
    plt.title(i)
    plt.show()