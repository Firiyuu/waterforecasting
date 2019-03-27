import pandas as pd
import time
import datetime
from imptation import imputation_mean, imputation_k #Recieves MATRIX string 
from normalization import normalization, transform
from feature_selection import feature_selection
import csv
import pprint
import numpy as np
import math


def time_to_value(value):
  timestr = value
  ftr = [3600,60,1]
  converted = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
  return converted



data = pd.read_csv("Mandulog.csv")
# Preview the first 5 lines of the loaded data 
df_list = data['TIME'].tolist()
df_list_wl = data['WATERLEVEL'].tolist()

length_list = len(df_list)
print "Before imputation: " + str(length_list)


peak = []
accepted = []
rejected = []
odd = []



rows_list = []
rows_list_wl = []
indeces = []

# While iterating through indices and values, use enumerate
for i in range(0, len(df_list)):       # iterate through all indices


    pre = df_list[i-1]
    post = df_list[i]
    bring_along = df_list_wl[i]


    rows_list_wl.append(bring_along)
    rows_list.append(post)

    #print ("Selected >> Pre: {}, Post: {}".format(pre,post)) # updated the print line to make it more readable
    

    value_pre = time_to_value(pre)
    value_x = time_to_value(post)

    
    #print str(value_pre) + ' - ' + str(value_x)

    if value_x < 0 or value_pre < 0:
        #print str(value_pre) + ' - ' + str(value_x)
        break



    in_between = value_x - value_pre

    #TODO Post-Pre/10 = n-rows to be imputed within to put 'NaN'
    n_rows = in_between/600

    if (len(str(value_pre)) == 2 and len(str(value_x)) == 5) or (len(str(value_x)) == 2 and len(str(value_pre)) == 5):
        continue
    else:  





 
        if in_between == 600:
          accepted.append({value_pre, value_x}) 
        elif in_between < 0:
          odd.append({value_pre, value_x, in_between})
        else:
          rejected.append({value_pre, value_x, i, i-1})
          #Declare blanks as NaN -- Toinclude n_rows

          for i in n_rows:
            rows_list.append('NaN')
            rows_list_wl.append('NaN')



all_rows = []
matrix_tempo = []

for i in range(0, len(rows_list)):
    if rows_list[i] == 'NaN' and rows_list_wl[i]=='NaN':
       indeces.append(str(i))
    
    try:
        string = str(time_to_value(str(rows_list[i]))) + ',' + str(rows_list_wl[i])
        all_rows.append(string)
    except Exception as e:
        string = (str(rows_list[i])) + ',' + str(rows_list_wl[i])
        matrix_tempo.append([rows_list[i],float(rows_list_wl[i])])
        all_rows.append(string)		




for index in indeces:

	pre = int(index)-1
	try:
		print "Before: " + str(all_rows[int(index)]) + '-' + str(all_rows[int(index)-1])
		all_rows[int(index)], all_rows[pre] = all_rows[pre], all_rows[int(index)]
		print "After: " + str(all_rows[int(index)]) + '-' + str(all_rows[int(index)-1])


	except Exception as e:
		print str(e)
		break


matrice  = []
with open('nan.csv', 'w') as f:
	for i in range(0, len(all_rows)):
           string = str(all_rows[i])

           row_ = all_rows[i].split(',')

           try:
              first_  = int(row_[0])
              next_  = float(row_[-1])
           except:
           	  row1 = float('NaN')
           	  row2 = float('NaN')
           	  first_ = row1
           	  next_ = row2

           matrice.append([first_,next_])
           f.write(string + '\n')



df = pd.DataFrame(matrice, columns=['TIME', 'WATERLEVEL'])
print str(df)

matrix_final = np.array(df)
matrix_imputed = imputation_mean(matrix_final)



#imputation_k(matrix_final)


# matrix_normalized = normalization(matrix_imputed)

# matrix_transformed = transform(matrix_normalized)

# feature_selection = feature_selection(matrix_transformed)


print "Data preparation completed"
# print "Accepted values: " + str(len(accepted))
# print "Rejected values: " + str(len(rejected))
# print "Odd values: " + str(len(odd))

# f= open("accepted.txt","w+")
# f.write(str(accepted))
# f.close() 

 
# f= open("rejected.txt","w+")
# f.write(str(rejected))
# f.close() 


# f= open("odd.txt","w+")
# f.write(str(odd))
# f.close() 


# #For imputation we would only need Water Level and Time

# print "After imputation: " + str(len(rows_list))