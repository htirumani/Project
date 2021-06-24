from datetime import datetime
import pandas as pd
import numpy as np
from pprint import pprint
from matplotlib import pyplot as plt

path = 'Data Analysis/processed-data-files/all_df_clean.csv'
df = pd.read_csv(path, index_col=0, parse_dates=['DATE'])

times = df['DATE'].to_list()
hours = [int(t.hour < 9 or t.hour > 21) for t in times]

# 0 for 9am-9pm, 1 else
df['NIGHTTIME'] = hours
df.to_csv('user1_featured.csv')