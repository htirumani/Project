import numpy as np
import pandas as pd
import datetime
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import os

from utils import custom_train_test_split, get_user_predictions

from pprint import pprint

features = ['HEART', 'STEP', 'ACTIVITY', '10MIN_STEP_SUM', 'MINFROMMIDNIGHT', 'PSLEEP']
label = '5MIN_SLEEP_PROB'

# get train and test sets
split_prop = 0.30
data_path = 'Data Analysis/Dataset/final/'
fps = os.listdir(data_path)
fps.remove('combined')
fps.remove('validation')

paths = [data_path + f for f in fps]
X_test, y_test, X_train, y_train = custom_train_test_split(features, paths, label=label, split_prop = split_prop, dropna=True)

# get validation set
val_path = data_path + 'validation/'
val_paths = [val_path + f for f in os.listdir(val_path)]
X_val, y_val, _, _ = custom_train_test_split(features, val_paths, 1.0) # get all validation data in one df

# define and fit Decision Tree model
model = GradientBoostingRegressor(
    loss = 'ls',
    learning_rate=0.1,
    max_depth=30,
    n_estimators=25,
    min_samples_split=5000,
    random_state=0,
    ).fit(X_train, y_train)

# print model performance
print('Training Loss: ', model.score(X_train, y_train))
print('Testing Loss: ', model.score(X_test, y_test))

get_user_predictions(model, features, data_path, 'reg_preds/', label)