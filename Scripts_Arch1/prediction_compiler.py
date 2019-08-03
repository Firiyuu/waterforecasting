import pandas as pd
import pandas as pd
import numpy as np


data = pd.read_csv('prediction_day1.csv')


list_data = data['predictions'].to_list()


list_of_lists = []

count = 0

list_ = []

for data_ in list_data:
	if count == 48:
		count = 0
		list_of_lists.append(list_)
		
		print("Finished " + str(list_data.index(data_)) + " length " + str(len(list_)))
		print("Length of all list: " + str(len(list_of_lists)))

		list_[:] = []


	else:
		count+=1
		list_.append(data_)


dataframe = pd.DataFrame.from_records(list_of_lists)
print(dataframe)