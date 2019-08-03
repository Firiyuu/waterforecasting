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


def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100



# def analyze(series):

# 	series['DATETIME'] = pd.to_datetime(series['DATETIME'])
# 	series['DATE'] = [d.date() for d in series['DATETIME']]
# 	series['TIME'] = [d.time() for d in series['DATETIME']]
# 	series['WATERLEVEL'] = series['WATERLEVEL']/1000


	 

# 	series['DATE'] = pd.to_datetime(series['DATE'])
# 	series['MONTH'] =   series['DATE'].dt.to_period('M')



# 	series['YEAR'] = pd.DatetimeIndex(series['DATE']).year
# 	series['MONTH'] = pd.DatetimeIndex(series['DATE']).month
# 	series['DAY'] = pd.DatetimeIndex(series['DATE']).day


# 	series['DATETIME'] = (series['DATETIME'] - series['DATETIME'].min())  / np.timedelta64(1,'D')
# 	series['DATE'] = pd.to_datetime(series['DATE'])
# 	series['DATE'] =  (series['DATE'] - series['DATE'].min())  / np.timedelta64(1,'D')
# 	series['TIME'] =  series['DATETIME'] - series['DATE']




# 	series = series.drop(columns="DATETIME")
# 	series = series.drop(columns="DAY")

# 	scaler = MinMaxScaler()
# 	scaler.fit(series)
# 	series = scaler.transform(series)
# 	series = pd.DataFrame(series, columns=['WATERLVEL','RF_DIGKILAAN','RF_ROGONGON', 'DAY', 'TIME', 'MONTH', 'YEAR'])
# 	print(series.head())

# 	return series


def analyze(series):

	series['DATETIME'] = pd.to_datetime(series['DATETIME'])
	series['DATE'] = [d.date() for d in series['DATETIME']]
	series['TIME'] = [d.time() for d in series['DATETIME']]
	series['WATERLEVEL'] = series['WATERLEVEL']/1000


	 

	series['DATE'] = pd.to_datetime(series['DATE'])
	series['MONTH'] =   series['DATE'].dt.to_period('M')



	series['YEAR'] = pd.DatetimeIndex(series['DATE']).year
	series['MONTH'] = pd.DatetimeIndex(series['DATE']).month
	series['DAY'] = pd.DatetimeIndex(series['DATE']).day


	series['DATETIME'] = (series['DATETIME'] - series['DATETIME'].min())  / np.timedelta64(1,'D')
	series['DATE'] = pd.to_datetime(series['DATE'])
	series['DATE'] =  (series['DATE'] - series['DATE'].min())  / np.timedelta64(1,'D')
	series['TIME'] =  series['DATETIME'] - series['DATE']




	series = series.drop(columns="DATETIME")
	series = series.drop(columns="MONTH")
	series = series.drop(columns="YEAR")
	series = series.drop(columns="DATE")

	print(series.head())

	scaler = MinMaxScaler()
	scaler.fit(series)
	series = scaler.transform(series)
	series = pd.DataFrame(series, columns=['WATERLVEL','RF_DIGKILAAN','RF_ROGONGON','W1','R1','D1','W2','R2','D2','W3','R3','D3','DAY', 'TIME'])
	print(series.head())

	return series


def train(series, series1, series3):
	print("---------- Training")
	print(series)
	
	

	scaler = MinMaxScaler()
	scaler.fit(series)
	scaler.fit(series1)
	scaler.fit(series3)

	series = scaler.transform(series)
	series = scaler.transform(series1)
	series = scaler.transform(series3)

	print("---------- Transformed")
	print(series)

	series = pd.DataFrame(series, columns=['WATERLVEL','RF_DIGKILAAN','RF_ROGONGON','W1','R1','D1','W2','R2','D2','W3','R3','D3','DAY', 'TIME'])


	print("---------- New Dataframe")
	print(series)


	series = series[['WATERLVEL','RF_DIGKILAAN','RF_ROGONGON','W1','R1','D1','W2','R2','D2','W3','R3','D3','DAY', 'TIME']]
	print("Normalized: ")
	print(series)

	series.to_csv('merge_normalized_ffffff1.csv')



	#P-value gives us the probability of finding an observation under an assumption that a particular hypothesis is true.
	#This probability is used to accept or reject that hypothesis.

	# Correlation is a statistical term which in common usage refers 
	# to how close two variables are to having a linear relationship with each other.
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

	return series


def predict(series):
	#PREDICTION
	print(series.head())

	X = series[['WATERLVEL','RF_DIGKILAAN','RF_ROGONGON','W1','R1','D1','W2','R2','D2','W3','R3','D3','DAY', 'TIME']]
	y = series[['WATERLVEL']]

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=101)

	lm = LinearRegression()
	lm.fit(X_train,y_train)

	predictions = lm.predict(X_test)


	plt.scatter(y_test,predictions)
	plt.show()

	predictions = lm.predict(series)
	series['PREDICTIONS'] = predictions
	series.to_csv('spearman_predict_f111.csv')



	X = series[['WATERLVEL','RF_DIGKILAAN','RF_ROGONGON','W1','R1','D1','W2','R2','D2','W3','R3','D3','DAY', 'TIME']]
	y = series[['WATERLVEL']]



	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=101)




	#GRID SEARCH CROSS VALIDATION
	parameters = {'kernel': ('linear', 'rbf','poly'), 'C':[1.5, 10],'gamma': [1e-7, 1e-4],'epsilon':[0.1,0.2,0.5,0.3]}

	svc = svm.SVR()
	clf = GridSearchCV(svc, parameters, cv=2)
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
	y_test = y_test*3.5
	rms = sqrt(mean_squared_error(y_test, predictions))
	mape = mean_absolute_percentage_error(y_test, predictions)
	print("\n\nRMSE Accuracy score: " + str(rms))
	print("\n\nMAPE Accuracy score: " + str(mape))
	plt.plot(y_test)
	plt.plot(predictions)
	plt.legend(["true", "pred"])
	plt.show()

	return predictions