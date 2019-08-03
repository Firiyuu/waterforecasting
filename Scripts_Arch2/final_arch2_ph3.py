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



from season import get_rainy, get_dry
from architecture_2_ph3 import analyze, train, predict
#NORMALIZATION





def represent(series):
	series_ = series['TIME']
	series_list = series_.tolist()

	new_list = []

	counter = 0

	while counter != len(series_list):
			for i in range(1,49):
				counter+=1
				new_list.append(i)
	
	new_series = pd.Series(new_list)






	series = series.drop(columns=['TIME'])
	print("-----------------------")


	series['TIME'] = new_series
	print(len(series))

	return series






series1 = pd.read_csv('phase1.csv')
series2 = pd.read_csv('phase2.csv')
series3 = pd.read_csv('phase3.csv')
series1 = series1.fillna(0)
series2 = series2.fillna(0)
series3 = series3.fillna(0)



#12 to 5
series_rainy1 = get_rainy(series1)
series_rainy2 = get_rainy(series2)
series_rainy3 = get_rainy(series2)
rainy1 = analyze(series_rainy1)
rainy2 = analyze(series_rainy2)
rainy3 = analyze(series_rainy3)



trained = train(rainy1, rainy2, rainy3)


predictions = predict(trained)
ser = pd.Series(predictions)
ser.to_csv('prediction_series.csv')
print("Length: " + str(len(predictions)))
prediction = pd.DataFrame(predictions, columns=['predictions']).to_csv('prediction_architecture2_phase3.csv')



# #6 to 11
# series_dry = get_dry(series)
# dry_ = analyze(series_dry)
# print(dry_.head())
# train(dry_)
# print(len(dry_))
# predictions_ = predict(dry_)
# print(predictions_)






