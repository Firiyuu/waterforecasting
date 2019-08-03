import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing  import Normalizer
#TRAIN
rainfall = pd.read_csv('Digkilaan_interpol.csv')
rainfall.columns = ['DATETIME','RAINFALL']
rainfall['RAINFALL'] = rainfall['RAINFALL']
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



# #INPUT WATERLEVEL
waterlevel = pd.read_csv('Mandulog_interpol.csv')
waterlevel.columns = ['DATETIME','WATERLEVEL']
waterlevel['WATERLEVEL'].interpolate(method='linear', inplace=True)
waterlevel['DATETIME'] = pd.to_datetime(waterlevel['DATETIME'])
waterlevel['WATERLEVEL'] = waterlevel['WATERLEVEL']*1000
waterlevel.to_csv('Mandulog_imputed.csv')



#INPUT RAINFALL
rainfall = pd.read_csv('Digkilaan_interpol.csv')
rainfall.columns = ['DATETIME','RAINFALL']
rainfall['RAINFALL'].interpolate(method='linear', inplace=True)
rainfall['DATETIME'] = pd.to_datetime(rainfall['DATETIME'])
rainfall['RAINFALL'] = rainfall['RAINFALL']
rainfall.to_csv('Digkilaan_imputed.csv')

#MERGING


# #separate array into input and output components
# scaler = Normalizer().fit(merged_df)
# normalizedX = scaler.transform(merged_df)



# predictions = lm.predict(merged_df)
# merged_df['PREDICTIONS'] = predictions
# merged_df.to_csv('predicted.csv')
