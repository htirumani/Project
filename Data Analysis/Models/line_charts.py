# plot where y axis is feature and x is time.
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

ddir = 'Data Analysis/Dataset/final'
l = os.listdir(ddir)

l.remove('combined')
l.remove('validation')

# l.remove('all_clean.csv')

# l = ['user0_clean.csv']

for i in l:
    print(i)
    df = pd.read_csv(ddir + '/' + i, parse_dates=['DATE'])
    x = df['DATE']
    y = df['HEART']
    z = df['SLEEP'] * 30000
    w = df['STEP']
    v = df['ACTIVITY']

    plt.plot(x,z, color="red", alpha=0.5)
    plt.plot(x, v)
    plt.title(i)
    plt.show()