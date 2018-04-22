import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree

balance_data = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/balance-scale/balance-scale.data',
                           sep= ',', header= None)


print("Dataset Lenght:: ", len(balance_data))
print("Dataset Shape:: ", balance_data.shape)
print(balance_data.head())

X = balance_data.values[:, 1:5]
Y = balance_data.values[:,0]

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=100)

clf_gini = DecisionTreeClassifier(criterion="gini", random_state = 100, max_depth=3, min_samples_leaf=5)
clf_gini.fit(X_train, y_train)

DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=3,
                       max_features=None, max_leaf_nodes=None, min_samples_leaf=5,
                       min_samples_split=2, min_weight_fraction_leaf=0.0,
                       presort=False, random_state=100, splitter='best')


clf_entropy = DecisionTreeClassifier(criterion="entropy", random_state = 100, max_depth=3, min_samples_leaf=5)
clf_entropy.fit(X_train, y_train)
DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=3,
                       max_features=None, max_leaf_nodes=None, min_samples_leaf=5,
                       min_samples_split=2, min_weight_fraction_leaf=0.0,
                       presort=False, random_state=100, splitter='best')

print(clf_gini.predict([[4, 4, 3, 3]]))
print(clf_entropy.predict([[4, 4, 3, 3]]))

y_pred_gini = clf_gini.predict(X_test)
y_pred_entropy = clf_entropy.predict(X_test)

print("Gini accuracy is ", accuracy_score(y_test,y_pred_gini)*100)
print("Entropy accuracy is ", accuracy_score(y_test,y_pred_entropy)*100)