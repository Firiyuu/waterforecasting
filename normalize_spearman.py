from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV
from sklearn import svm, datasets
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from math import sqrt
#NORMALIZATION

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

series = pd.read_csv('merged_imputation.csv')
series['DATETIME'] = pd.to_datetime(series['DATETIME'])
series['DATETIME'] = pd.to_datetime(series['DATETIME'])
series['DATETIME'] = (series['DATETIME'] - series['DATETIME'].min())  / np.timedelta64(1,'D')

scaler = MinMaxScaler()
scaler.fit(series)
series = scaler.transform(series)
series = pd.DataFrame(series, columns=['DATETIME', 'RAINFALL', 'WATERLEVEL'])
print("Normalized: ")
print(series)
series.to_csv('merge_normalized.csv')
#P-value gives us the probability of finding an observation under an assumption that a particular hypothesis is true.
#This probability is used to accept or reject that hypothesis.

#Correlation is a statistical term which in common usage refers 
#to how close two variables are to having a linear relationship with each other.
print("-----------------\nFeature Selection: Spearman\n")
corr, p_value = spearmanr(series['WATERLEVEL'] , series['RAINFALL'] )
print("Correlation: " + str(corr))
print("P Value: " + str(p_value))





#PREDICTION
X = series[['DATETIME','RAINFALL','WATERLEVEL']]
y = series['WATERLEVEL']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)

print(X_test)

lm = LinearRegression()
lm.fit(X_train,y_train)

predictions = lm.predict(X_test)


plt.scatter(y_test,predictions)
plt.show()

predictions = lm.predict(series)
series['PREDICTIONS'] = predictions
series.to_csv('spearman_predict.csv')


series.to_csv('pearson_predict.csv')

X = series[['WATERLEVEL', 'RAINFALL']]
y = series['WATERLEVEL']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)




#GRID SEARCH CROSS VALIDATION
parameters = [{'kernel': ['rbf'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
                     'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
                    {'kernel': ['sigmoid'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
                     'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
                    {'kernel': ['poly'], 'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]}
                   ]

svc = svm.SVC(gamma="scale")
clf = GridSearchCV(svc, parameters, cv=5)
fitted = clf.fit(X_train.astype('int'), y_train.astype('int'))
print(fitted)


print("\nBest parameters set found on development set:\n")
print(clf.best_params_)
print("Grid scores on development set:")
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r"
          % (mean, std * 2, params))\

#VALIDATE VIA RMSE
predictions = clf.predict(X_test)
print(predictions)
rms = sqrt(mean_squared_error(y_test, predictions))
print("\n\nRMSE Accuracy score: " + str(rms))


mape = mean_absolute_percentage_error(y_test, predictions)
print("\n\nMAPE Accuracy score: " + str(mape))