from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#NORMALIZATION

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