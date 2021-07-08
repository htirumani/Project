# plot where y axis is feature and x is time.
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

clean_dir = 'Data Analysis/Dataset/clean'
l = os.listdir(clean_dir)
l.remove('all_clean.csv')

# l = ['user0_clean.csv']

for i in l:
    print(i)
    df = pd.read_csv(clean_dir + '/' + i, parse_dates=['DATE'])
    x = df['DATE']
    y = df['HEART']
    z = df['SLEEP'] * 150
    w = df['STEP']

    plt.plot(x,z, color="red", alpha=0.5)
    plt.plot(x, w)
    plt.title(i)
    plt.show()