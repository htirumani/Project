import numpy as np
import pandas as pd
import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from utils import custom_train_test_split

from pprint import pprint

u0_path = 'Data Analysis/Dataset/clean/user0_df_clean.csv'
u2_path = 'Data Analysis/Dataset/clean/user2_df_clean.csv'

split_prop = 0.85

X_train, y_train, X_test, y_test = custom_train_test_split(['HEART', 'STEP'], [u0_path, u2_path], split_prop)

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
