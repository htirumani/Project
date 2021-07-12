import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

df = pd.read_csv("activity_featured.csv", index_col=0, parse_dates=['DATE'])

X, y = df[['HEART', 'STEP', 'ACTIVITY']].to_numpy(), df['SLEEP'].to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

# fitting an SVM using a linear kernel

svclassifier = SVC(kernel='linear')
svclassifier.fit(X_train, y_train)

# prediction and evaluation
y_pred = svclassifier.predict(X_test)
print(accuracy_score(y_test, y_pred)*100)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))