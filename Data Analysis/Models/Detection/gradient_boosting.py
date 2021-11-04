import numpy as np
import pandas as pd
import datetime
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import os

from utils import custom_train_test_split, get_user_predictions

from pprint import pprint

features = ['HEART', 'STEP', 'ACTIVITY', '10MIN_STEP_SUM', 'MINFROMMIDNIGHT', '24HR_SLEEP_TOTAL']

# get train and test sets
split_prop = 0.30
data_path = 'Data Analysis/Dataset/final/'
fps = os.listdir(data_path)
fps.remove('combined')
fps.remove('validation')

paths = [data_path + f for f in fps]
X_test, y_test, X_train, y_train = custom_train_test_split(features, paths, split_prop)

# get validation set
val_path = data_path + 'validation/'
val_paths = [val_path + f for f in os.listdir(val_path)]
X_val, y_val, _, _ = custom_train_test_split(features, val_paths, 1.0) # get all validation data in one df

# define and fit Decision Tree model
model = GradientBoostingClassifier(
    learning_rate=0.1,
    loss='deviance',
    max_depth=30,
    n_estimators=25,
    min_samples_split=20000,
    random_state=0,
    ).fit(X_train, y_train)

# print model performance
print('Training Accuracy: ', model.score(X_train, y_train))
print('Testing Accuracy: ', model.score(X_test, y_test))

y_hat_train = model.predict(X_train)
y_hat_test = model.predict(X_test)
errs = y_hat_test != y_test
fn = y_test & np.logical_not(y_hat_test)
fp = np.logical_not(y_test) & y_hat_test

print()
print('Confusion Matrix\n', confusion_matrix(y_test, y_hat_test))

print()
print('Training Classification Report\n', classification_report(y_train, y_hat_train, digits=3))

print()
print('Testing Classification Report\n', classification_report(y_test, y_hat_test, digits=3))

print()
print('Testing Errors: {} / {}'.format(sum(errs), y_hat_test.shape[0]))
print('Num False Negatives:', sum(fn))
print('Num False Positives:', sum(fp))

y_hat_val = model.predict(X_val)

print()
print('Validation Accuracy: ', model.score(X_val, y_val))

print()
print('Confusion Matrix\n', confusion_matrix(y_val, y_hat_val))


print(model.feature_importances_)

get_user_predictions(model, features, data_path, '')