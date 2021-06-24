import datetime
import numpy as np
import pandas as pd
import pymongo
import json
import matplotlib.pyplot as plt
import ssl
import missingno as msno

# Pandas DataFrame
df = pd.read_csv("max_df.csv", index_col=0)
# cols: DATE, USER_ID, SLEEP, HEART, STEPS, WEIGHT, HEIGHT
# print the sum of missing values
print(df.isna().sum())
# first visualize missing values in each column.
msno.matrix(df, labels=True)
plt.show()
# then missing values as a bar chart.
msno.bar(df, labels=True)
plt.show()
# Does having or not having missing values for a variable correlate with that of others?
msno.heatmap(df, labels=True)
plt.show()

