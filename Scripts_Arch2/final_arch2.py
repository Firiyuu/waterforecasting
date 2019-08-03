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
from architecture_2 import analyze, train, predict
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






# series = pd.read_csv('phase1.csv')
series = pd.read_csv('phase1.csv')
series = series.fillna(0)





#12 to 5
series_rainy = get_rainy(series)
rainy = analyze(series_rainy)
#rainy = represent(rainy)
train(rainy)



predictions = predict(rainy)
ser = pd.Series(predictions)
ser.to_csv('prediction_series.csv')
print("Length: " + str(len(predictions)))
prediction = pd.DataFrame(predictions, columns=['predictions']).to_csv('prediction_architecture2_phase1.csv')



# #6 to 11
# series_dry = get_dry(series)
# dry_ = analyze(series_dry)
# print(dry_.head())
# train(dry_)
# print(len(dry_))
# predictions_ = predict(dry_)
# print(predictions_)






