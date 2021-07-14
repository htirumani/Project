import numpy as np
import pandas as pd
import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, make_scorer, precision_score, recall_score, accuracy_score

from utils import custom_train_test_split
import os

from pprint import pprint

features = ['HEART', 'STEP', 'ACTIVITY', '10MIN_STEP_SUM', 'MINFROMMIDNIGHT']

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

model = RandomForestClassifier(
    criterion='entropy',
    n_estimators=100,
    max_depth=20,
    min_samples_split=10000,
    class_weight='balanced',
    random_state=3).fit(X_train, y_train)

# print model performance
print('Training Accuracy: ', model.score(X_train, y_train))
print('Testing Accuracy: ', model.score(X_test, y_test))

y_hat = model.predict(X_test)
errs = y_hat != y_test
fn = y_test & np.logical_not(y_hat)
fp = np.logical_not(y_test) & y_hat

print()
print('Confusion Matrix\n', confusion_matrix(y_test, y_hat))

print()
print('Classification Report\n', classification_report(y_test, y_hat))

print()
print('Testing Errors: {} / {}'.format(sum(errs), y_hat.shape[0]))
print('Num False Negatives:', sum(fn))
print('Num False Positives:', sum(fp))

y_hat_val = model.predict(X_val)

print()
print('Validation Accuracy: ', model.score(X_val, y_val))

print()
print('Confusion Matrix\n', confusion_matrix(y_val, y_hat_val))
