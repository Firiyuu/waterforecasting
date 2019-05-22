import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#TRAIN
rainfall = pd.read_csv('Digkilaan_interpol.csv')
rainfall.columns = ['DATETIME','RAINFALL']
rainfall['RAINFALL'] = rainfall['RAINFALL']*10
rainfall['DATETIME'] = pd.to_datetime(rainfall['DATETIME'])
rainfall['DATETIME'] = (rainfall['DATETIME'] - rainfall['DATETIME'].min())  / np.timedelta64(1,'D')

rainfall.head()
rainfall.info()
rainfall.describe()



#DROP EMPTY CELL
rainfall['RAINFALL'].replace('', np.nan, inplace=True)
rainfall.dropna(subset=['RAINFALL'], inplace=True)
sns.pairplot(rainfall)
sns.distplot(rainfall['RAINFALL'])




X = rainfall[['DATETIME','RAINFALL']]
y = rainfall['RAINFALL']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)

print(X_test)

lm = LinearRegression()
lm.fit(X_train,y_train)

predictions = lm.predict(X_test)
print(predictions)

plt.scatter(y_test,predictions)
plt.show()



#INPUT
waterlevel = pd.read_csv('Mandulog_interpol.csv')
waterlevel.columns = ['DATETIME','WATERLEVEL']
waterlevel['WATERLEVEL'].interpolate(method='linear', limit_direction ='backward', inplace=True)
waterlevel['DATETIME'] = pd.to_datetime(waterlevel['DATETIME'])
waterlevel['DATETIME'] = (waterlevel['DATETIME'] - waterlevel['DATETIME'].min())  / np.timedelta64(1,'D')
predictions = lm.predict(waterlevel)

waterlevel['PREDICTIONS'] = predictions
waterlevel.to_csv('Mandulog_predicted.csv')
