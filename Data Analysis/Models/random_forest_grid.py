import numpy as np
import pandas as pd
import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, make_scorer, precision_score, recall_score, accuracy_score

from utils import custom_train_test_split

from pprint import pprint

u0_path = 'Data Analysis/Dataset/final/user0_featured.csv'
u2_path = 'Data Analysis/Dataset/final/user2_featured.csv'
split_prop = 1.0

X_train, y_train, X_test, y_test = custom_train_test_split(['HEART', 'STEP', 'NIGHTTIME', 'MEAN_10MIN_HR', 'SD_10MIN_HR'], [u0_path, u2_path], split_prop)

criterion = ['gini', 'entropy']
max_depth = [2, 4, 6, 8, 10, 12]
n_estimators = [50, 100, 200]
params = {'criterion': criterion, 'max_depth': max_depth, 'n_estimators': n_estimators}
scoring = {'accuracy': make_scorer(accuracy_score), 'precision': make_scorer(precision_score), 'recall': make_scorer(recall_score)}

grid = GridSearchCV(RandomForestClassifier(), params, scoring=scoring, refit=False).fit(X_train, y_train)

results = pd.DataFrame(grid.cv_results_)
