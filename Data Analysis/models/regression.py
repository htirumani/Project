import numpy as np
import pandas as pd
import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from pprint import pprint

path = 'Data Analysis/processed-data-files/all_featured.csv'

df = pd.read_csv(path, index_col=0, parse_dates=['DATE'])

X, y = df[['HEART', 'STEP', 'WEIGHT', 'HEIGHT', 'NIGHTTIME']].to_numpy(), df['SLEEP'].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, train_size=0.9, test_size=0.1, shuffle=True)

model = LogisticRegression(random_state=0).fit(X_train, y_train)

print('Training Accuracy: ', model.score(X_train, y_train))
print('Testing Accuracy: ', model.score(X_test, y_test))

pprint(model.get_params())

# X_train -> model -> y_hat ----compare----> t_train -> percentage of correctly predicted labels