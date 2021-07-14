import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import svm, datasets
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("all_featured.csv", index_col=0, parse_dates=['DATE'])
X = df[['HEART', 'STEP']].to_numpy()
y = df['SLEEP'].to_numpy()
h = 0.2

C = 1.0  # SVM regularization parameter
print("Fitting linear kernel...")
svc = svm.SVC(kernel='linear', C=C).fit(X, y)
print("Fitting gaussian kernel...")
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(X, y)
print("Fitting polynomial kernel...")
poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(X, y)

print("Creating the plots...")
# create a mesh to plot in
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
print("Still working on the plots...")
# title for the plots
titles = ['SVC with linear kernel',
          'SVC with RBF kernel',
          'SVC with polynomial (degree 3) kernel']

for i, clf in enumerate((svc, rbf_svc, poly_svc)):
    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    plt.subplot(2, 2, i + 1)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
    print("Plotting the training points...")
    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm)
    plt.xlabel('Sepal length')
    plt.ylabel('Sepal width')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())
    plt.title(titles[i])
print("Ready to show the plots...")
plt.show()
plt.ion()