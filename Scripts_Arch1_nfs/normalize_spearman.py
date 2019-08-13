from sklearn.preprocessing import MinMaxScaler, LabelEncoder
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

series = pd.read_csv('merged_imputation_f.csv')




series['DATETIME'] = pd.to_datetime(series['DATETIME'])
series['DATE'] = [d.date() for d in series['DATETIME']]
series['TIME'] = [d.time() for d in series['DATETIME']]
series['WATERLEVEL'] = series['WATERLEVEL']/1000
print(series)

 

series['DATE'] = pd.to_datetime(series['DATE'])
series['MONTH'] =   series['DATE'].dt.to_period('M')
print(series['MONTH'])





series['DATETIME'] = (series['DATETIME'] - series['DATETIME'].min())  / np.timedelta64(1,'D')
series['TIME'] =  series['DATETIME'] - series['DATE']





print(series)

scaler = MinMaxScaler()
scaler.fit(series)
series = scaler.transform(series)
series = pd.DataFrame(series, columns=['DATE','TIME', 'WATERLEVEL', 'RF_DIGKILAAN', 'RF_ROGONGON'])
series = series[['WATERLEVEL','DATE','TIME', 'RF_DIGKILAAN','RF_ROGONGON']]
print("Normalized: ")
print(series)

# series.to_csv('merge_normalized_ff.csv')
#P-value gives us the probability of finding an observation under an assumption that a particular hypothesis is true.
#This probability is used to accept or reject that hypothesis.

#Correlation is a statistical term which in common usage refers 
#to how close two variables are to having a linear relationship with each other.
print("-----------------\nFeature Selection: Spearman\n")
corr, p_value = spearmanr(series)
print("Correlation: " + str(corr))
print("P Value: " + str(p_value))
print(series)

#Using Pearson Correlation
print("-----------------\nFeature Selection: Pearson\n")
plt.figure(figsize=(12,10))
cor = series.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()



#PREDICTION

X = series[['DATE','TIME', 'WATERLEVEL', 'RF_DIGKILAAN', 'RF_ROGONGON']]
y = series[['WATERLEVEL']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=101)

lm = LinearRegression()
lm.fit(X_train,y_train)

predictions = lm.predict(X_test)


plt.scatter(y_test,predictions)
plt.show()

predictions = lm.predict(series)
series['PREDICTIONS'] = predictions
series.to_csv('spearman_predict_f111.csv')



# X = series[['DATETIME', 'DATE','TIME',  'WATERLEVEL', 'RF_DIGKILAAN', 'RF_ROGONGON']]
# y = series['WATERLEVEL']



# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=101)




# #GRID SEARCH CROSS VALIDATION
# parameters = [{'kernel': ['rbf'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
#                      'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
#                     {'kernel': ['sigmoid'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
#                      'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
#                     {'kernel': ['poly'], 'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]}
#                    ]

# svc = svm.SVC(gamma="scale")
# clf = GridSearchCV(svc, parameters, cv=2)
# fitted = clf.fit(X_train.astype('int'), y_train.astype('int'))
# print(fitted)


# print("\nBest parameters set found on development set:\n")
# print(clf.best_params_)
# print("Grid scores on development set:")
# means = clf.cv_results_['mean_test_score']
# stds = clf.cv_results_['std_test_score']
# for mean, std, params in zip(means, stds, clf.cv_results_['params']):
#     print("%0.3f (+/-%0.03f) for %r"
#           % (mean, std * 2, params))\

# #VALIDATE VIA RMSE
# predictions = clf.predict(X_test)
# print(predictions)
# rms = sqrt(mean_squared_error(y_test, predictions))
# print("\n\nRMSE Accuracy score: " + str(rms))


