import numpy as np
import pandas as pd
import datetime
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import os
from sklearn.metrics import r2_score

from utils import custom_train_test_split, get_user_predictions

from pprint import pprint

features = ['HEART', 'STEP', 'ACTIVITY', '10MIN_STEP_SUM', 'PSLEEP']
label = '30MIN_SLEEP_PROB'

# get train and test sets
split_prop = 0.70
data_path = 'Data Analysis/Dataset/final/'
fps = os.listdir(data_path)
fps.remove('combined')
fps.remove('validation')

paths = [data_path + f for f in fps]
X_train, y_train, X_test, y_test = custom_train_test_split(features, paths, label=label, split_prop = split_prop, dropna=True)

# get validation set
val_path = data_path + 'validation/'
val_paths = [val_path + f for f in os.listdir(val_path)]
X_val, y_val, _, _ = custom_train_test_split(features, val_paths, 1.0) # get all validation data in one df

# define and fit Decision Tree model
model = GradientBoostingRegressor(
    loss = 'ls',
    learning_rate=0.0125,
    max_depth=15,
    n_estimators=100,
    min_samples_split=2500,
    random_state=0,
    ).fit(X_train, y_train)

train_preds = model.predict(X_train)
test_preds = model.predict(X_test)

print('Training Loss: ', r2_score(train_preds, y_train))
print('Testing Loss: ', r2_score(test_preds, y_test))

# print model performance
# print('Training Loss: ', model.score(X_train, y_train))
# print('Testing Loss: ', model.score(X_test, y_test))

print(model.feature_importances_)

# get_user_predictions(model, features, data_path, 'reg_preds/', label)