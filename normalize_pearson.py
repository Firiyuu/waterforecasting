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


#Using Pearson Correlation
print("-----------------\nFeature Selection: Pearson\n")
plt.figure(figsize=(12,10))
cor = series.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()


#Correlation with output variable
cor_target = abs(cor["WATERLEVEL"])

#Selecting highly correlated features
relevant_features = cor_target[cor_target>0.5]
print(relevant_features)
print(str(relevant_features) + ' is/are highly correlated with the output variable WATERLEVEL')

#Check the correlation of selected features with each other
print('\nCheck the correlation of selected features with each other\n')
print(series[["DATETIME","WATERLEVEL"]].corr())
print(series[["DATETIME","RAINFALL"]].corr())
print(series[["WATERLEVEL","RAINFALL"]].corr())


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
print(predictions)
series['PREDICTION'] = predictions

series.to_csv('pearson_predict.csv')