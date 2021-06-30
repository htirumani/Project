import numpy as np
import pandas as pd
import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, make_scorer, precision_score, recall_score, accuracy_score

from utils import custom_train_test_split

from pprint import pprint

u0_path = 'Data Analysis/Dataset/final/user0_featured.csv'
u2_path = 'Data Analysis/Dataset/final/user2_featured.csv'
split_prop = 1.0

X_train, y_train, X_test, y_test = custom_train_test_split(['HEART', 'STEP', 'NIGHTTIME', 'MEAN_10MIN_HR', 'SD_10MIN_HR'], [u0_path, u2_path], split_prop)

criterion = ['gini', 'entropy']
max_depth = [2,4,6,8,10,12]
params = {'criterion': criterion, 'max_depth': max_depth}
scoring = {'accuracy': make_scorer(accuracy_score), 'precision': make_scorer(precision_score), 'recall': make_scorer(recall_score)}

grid = GridSearchCV(DecisionTreeClassifier(), params, scoring=scoring, refit=False).fit(X_train, y_train)

results = pd.DataFrame(grid.cv_results_)
print(results)




# print model performance
# print('Training Accuracy: ', model.score(X_train, y_train))
# print('Testing Accuracy: ', model.score(X_test, y_test))

# y_hat = model.predict(X_test)
# errs = y_hat != y_test
# fn = y_test & np.logical_not(y_hat)
# fp = np.logical_not(y_test) & y_hat

# print()
# print('Confusion Matrix\n', confusion_matrix(y_test, y_hat))

# print()
# print('Classification Report\n', classification_report(y_test, y_hat))

# print()
# print('Testing Errors: {} / {}'.format(sum(errs), y_hat.shape[0]))
# print('Num False Negatives:', sum(fn))
# print('Num False Positives:', sum(fp))

# print()
# print('False Negative Rate: ', sum(fn) / sum(y_test))
# print('False Positive Rate: ', sum(fp) / sum(np.logical_not(y_test)))
