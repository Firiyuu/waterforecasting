import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



series = pd.read_csv('Digkilaan_trimmed.csv')
series['date_and_time'] = series['YEAR'].map(str) + '-'+ series['MONTH'].map(str) + '-'+ series['DAY'].map(str) + ' ' + series['TIME'].map(str)


date_and_time = series['date_and_time'].tolist()
rainfall = series['RAINFALL']
waterlevel = rainfall
waterlevel = waterlevel.tolist()

values = waterlevel
timestamps = pd.to_datetime(date_and_time)

ts = pd.Series(values, index=timestamps)
ts = ts.resample('15T').mean()

ts.interpolate(method='spline', order=3).plot()
ts.interpolate(method='time').plot()
ts.interpolate(method='linear', inplace=True)


print(str(ts))
ts.columns = ['DATETIME', 'RAINFALL']
ts.to_csv('Digkilaan_interpol.csv')
lines, labels = plt.gca().get_legend_handles_labels()
labels = ['spline', 'time']
plt.legend(lines, labels, loc='best')
plt.show()


