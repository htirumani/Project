import numpy as np
import pandas as pd
import datetime
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import os
from sklearn.metrics import r2_score

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

from utils import custom_train_test_split, get_user_predictions
from visualize_dt import show_tree

from pprint import pprint

features = ['HEART', 'ACTIVITY', '10MIN_STEP_SUM', 'MINFROMMIDNIGHT', '24HR_SLEEP_TOTAL']
label = '30MIN_SLEEP_PROB'

# get train and test sets
split_prop = 0.30
data_path = 'Data Analysis/Dataset/final/'
fps = os.listdir(data_path)
fps.remove('combined')
fps.remove('validation')

paths = [data_path + f for f in fps]
X_test, y_test, X_train, y_train = custom_train_test_split(features, paths, label=label, split_prop=split_prop, dropna=True)

X_train, y_train = SMOTE(sampling_strategy=0.25).fit_resample(X_train, y_train)
X_train, y_train = RandomUnderSampler(sampling_strategy=0.5).fit_resample(X_train, y_train)

# get validation set
val_path = data_path + 'validation/'
val_paths = [val_path + f for f in os.listdir(val_path)]
X_val, y_val, _, _ = custom_train_test_split(features, val_paths, 1.0) # get all validation data in one df

# define and fit Decision Tree model
model = GradientBoostingClassifier(
    learning_rate=0.075,
    max_depth=5,
    n_estimators=100,
    min_samples_split=2500,
    min_samples_leaf=150,
    random_state=34,
    ).fit(X_train, y_train)

train_preds = model.predict(X_train)
test_preds = model.predict(X_test)

print()
print('FEATURES: ', features)
print('IMPORTANCES: ', model.feature_importances_)

print()
print('Training Accuracy: ', model.score(X_train, y_train))
print('Testing Accuracy: ', model.score(X_test, y_test))

print()
print('Training Classification Report\n', classification_report(y_train, train_preds, digits=3))

print('Testing Classification Report\n', classification_report(y_test, test_preds, digits=3))

val_preds = model.predict(X_val)

print()
print('Validation Classification Report:\n', classification_report(y_val, val_preds, digits=3))

get_user_predictions(model, features, data_path, 'reg_preds/', label, get_probs=True)

# m = int(len(model.estimators_) / 2)

# tree0 = model.estimators_[0, 0]
# treem = model.estimators_[m, 0]
# treef = model.estimators_[-1, 0]

# show_tree(tree0, 'tree0.png')
# show_tree(treem, 'treem.png')
# show_tree(treef, 'treef.png')