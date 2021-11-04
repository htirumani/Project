# plot where y axis is feature and x is time.
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

import matplotlib as mpl
mpl.rc('image', cmap='bwr')

ddir = 'reg_preds'
l = os.listdir(ddir)
users = [i[:-10] for i in l]

ddir2 = 'Data Analysis/Dataset/final'


# l.remove('combined')
# l.remove('validation')

# l.remove('all_clean.csv')

# l = ['user2347167796_featured.csv']
# l = l[0:1]

users = [5577150313]

for u in users:
    print(u)
    df = pd.read_csv(ddir + '/' + '{}_preds.csv'.format(u), parse_dates=['DATE'])[314:5000]
    # df2 = pd.read_csv(ddir2 + '/' + 'user{}_featured.csv'.format(u), parse_dates=['DATE'])
    d = df['DATE']
    heart = df['HEART']
    step = df['STEP']
    activity = df['ACTIVITY']
    psleep = df['PSLEEP']
    step10min = df['10MIN_STEP_SUM']
    midnight = df['MINFROMMIDNIGHT']

    # sleep = df2['SLEEP']
    # sleep.to_csv('test.csv')

    near_sleep = df['30MIN_SLEEP_PROB'] == 1
    awake = df['30MIN_SLEEP_PROB'] == 0
    asleep = df['30MIN_SLEEP_PROB'] == -1

    preds = df['PRED']
    probs = df['PROBS']

    probs_list = df['PROBS'].tolist()
    asleep_list = asleep.to_list()
    pred_probs = [p if s != 1 else None for p, s in zip(probs_list, asleep_list)]

    mult = 1

    plt.figure(figsize=(8, 1))
    plt.stem(d, asleep * mult, markerfmt=' ', linefmt='lightgray', basefmt='white')
    plt.stem(d, near_sleep * mult, markerfmt=' ', linefmt='lightcoral', basefmt='white')
    plt.stem(d, awake * mult, markerfmt=' ', linefmt='lightsteelblue', basefmt='white')
    
    plt.scatter(d, pred_probs * mult, s=7, c=preds, zorder=2, alpha=0.4, linewidth=0.5)
    # plt.scatter(d, psleep, s=3, c='black', zorder=2, alpha=0.7, linewidth=0.5)

    plt.hlines(0.5, xmin=d.min(), xmax=d.max(), colors='dimgrey', linestyles='dashed')
    plt.title('Prediction Model Sample Results')
    plt.xlabel('Time')
    plt.ylabel('Predicted Probability')
    plt.show()