import numpy as np
import pandas as pd
import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from pprint import pprint

'''
We'll import the data from each user seperately, so we can do a train-test split before shuffling.
This way the model is tested on periods of time not yet seen.
'''
u0_path = 'Data Analysis/processed-data-files/user0_df_clean.csv'
u2_path = 'Data Analysis/processed-data-files/user2_df_clean.csv'

u0_df = pd.read_csv(u0_path, index_col=0, parse_dates=['DATE'])
u2_df = pd.read_csv(u2_path, index_col=0, parse_dates=['DATE'])

# split data to train and test dfs
u0_split = int(u0_df.shape[0] * 0.7)
u2_split = int(u2_df.shape[0] * 0.7)

u0_train = u0_df[:u0_split]
u0_test = u0_df[u0_split:]
u2_train = u2_df[:u2_split]
u2_test = u2_df[u2_split:]

# aggregate train and test sets to numpy arrays, split to features and labels
X_train = np.concatenate((u0_train[['HEART', 'STEP']].to_numpy(), u2_train[['HEART', 'STEP']].to_numpy()))
y_train = np.concatenate((u0_train['SLEEP'].to_numpy(), u2_train['SLEEP'].to_numpy()))

# shuffle X_train and y_train keeping features and labels aligned
shuffle = np.array(list(range(X_train.shape[0])))
np.random.shuffle(shuffle)
X_train = X_train[shuffle]
y_train = y_train[shuffle]

X_test = np.concatenate((u0_test[['HEART', 'STEP']].to_numpy(), u2_test[['HEART', 'STEP']].to_numpy()))
y_test = np.concatenate((u0_test['SLEEP'].to_numpy(), u2_test['SLEEP'].to_numpy()))

# define and fit Logistic Regression model
model = LogisticRegression(random_state=0).fit(X_train, y_train)

# print model performance
print('Training Accuracy: ', model.score(X_train, y_train))
print('Testing Accuracy: ', model.score(X_test, y_test))

print()
print('Model Coefficients: ', model.coef_.squeeze().tolist())

y_hat = model.predict(X_test)
errs = y_hat != y_test
fn = y_test & np.logical_not(y_hat)
fp = np.logical_not(y_test) & y_hat

print()
print('Testing Errors: {} / {}'.format(sum(errs), y_hat.shape[0]) )
print('Num False Negatives:', sum(fn))
print('Num False Positives:', sum(fp))

print()
print('False Negative Rate: ', sum(fn) / sum(y_test))
print('False Positive Rate: ', sum(fp) / sum(np.logical_not(y_test)))
