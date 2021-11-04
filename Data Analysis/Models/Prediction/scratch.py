import numpy as np
from sklearn.model_selection import train_test_split

X = np.array(list(range(20)))
y = np.array(list(range(20)))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, shuffle=False)

print(X_test, y_train)