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
from knn import impute_knn
from mongodb import save_to_db
import pymongo
# def define_time(array_):



def time_to_value(value):
  timestr = value
  ftr = [3600,60,1]
  converted = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
  return converted


def grouped_range(list_):

  group_of_groups = []
  group = []
  begin = []
  after = []
  counter = 0


  for i in range(len(all_rows)):

      string = str(all_rows[i])

      row_ = all_rows[i].split(',')

      try:
        row_after = all_rows[i+1].split(',')
      except Exception as e:
        print str(e)

      first_  = int(row_[0])
      first_after = int(row_after[0])
      next_  = row_[-1]

      if first_after > first_:
        if row_[1] == '':
           row_[1] = ''
           group.append(row_)
        else:
           row_[1] = float(row_[1])
           group.append(row_)
      else:
        try:
             #GET ORIGIN
             origin = group[0]
             origin = int(origin[0])

             if origin != 0:
                distance = origin/600
                for i in range(distance):
                  row_ = [600*i, '']
                  begin.append(row_)


             #GET LAST
             last = group[len(group)-1]
             last = int(last[0])

             if last != 85200:

                distance =  (85200-last)/600
                for i in range(distance):
                  row_ = [last + (600*i), '']
                  after.append(row_)

             group = begin + group + after


         
             #print("Legth of group: " + str(group))
             counter += 1
             print("Imputation in progress... " + str(counter))



           
             data=pd.DataFrame(group, columns=['Timestamp','Waterlevel'])

             data.loc[data['Waterlevel'] == '','Waterlevel'] = np.nan
             data.insert(0, 'TimeframeId', range(0,len(data)))


             data.to_csv('nan2.csv')
             data = pd.read_csv("nan2.csv")



             value = impute_knn(data)
             value = value['Waterlevel']

       

             data['Waterlevel'] = value
             

             filename = 'data' + str(counter) + '.csv'
             data.to_csv(filename)


             data.to_csv('mandulog_imputd.csv', mode="a", header=False)

             csvfile = open(str(filename), 'r')
             reader = csv.DictReader(csvfile)
             myclient = pymongo.MongoClient("mongodb://localhost:27017/")

             db=myclient.forecasting
             db.mandulog.drop()
             header= ["Timestamp", "Waterlevel"]

             for each in reader:
                 row={}
                 for field in header:
                     row[field]=each[field]

                 db.mandulog.insert(row)

             group = []
             after = []
             begin = []
             # try:
             #    value = impute_knn(data)
             #    print(str(value))
                

             # except MemoryError as e:

             #         print "Memory Error, saving to csv for manual inspection"
             #         df_ = pd.DataFrame([['----']])
             #         data.append(df_)
             #         data.to_csv('memorryerror.csv')
        except Exception as e:
          print(str(e))
          file1 = open("errors.txt","a")
          file1.write(str(e))
          file1.close() 

  print("Imputation Complete")
        



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
          
          for i in range(int(n_rows)-1):
             value_pre += 600
             rows_list.append(value_pre)
             rows_list_wl.append('')



all_rows = []
matrix_tempo = []

for i in range(0, len(rows_list)):
    if rows_list_wl[i]=='':
       indeces.append(str(i))
    
    try:


        condition_ = isinstance(rows_list[i], int)

        if condition_:
          string = str(str(rows_list[i])) + ',' + str(rows_list_wl[i])
          all_rows.append(string)


        else:
          string = str(time_to_value(str(rows_list[i]))) + ',' + str(rows_list_wl[i])
          all_rows.append(string)

    
    except Exception as e:
        string = (str(rows_list[i])) + ',' + str(rows_list_wl[i])
        matrix_tempo.append([rows_list[i],float(rows_list_wl[i])])
        all_rows.append(string)                




for index in indeces:

        pre = int(index)-1
        try:
                #print "Before: " + str(all_rows[int(index)]) + '-' + str(all_rows[int(index)-1])
                all_rows[int(index)], all_rows[pre] = all_rows[pre], all_rows[int(index)]
                #print "After: " + str(all_rows[int(index)]) + '-' + str(all_rows[int(index)-1])


        except Exception as e:
                print str(e)
                break



grouped_range(all_rows)





   
#    #print(str(group))
   
# group_sample = group_of_groups[0]
# for group in group_sample:
#    print str(group)
#    time.sleep(2)
# time.sleep(5)









# matrice  = []
# with open('missing.csv', 'w') as f:
#         for i in range(0, len(all_rows)):
#            string = str(all_rows[i])

#            row_ = all_rows[i].split(',')

#            try:
#               first_  = int(row_[0])


#               next_  = float(row_[-1])
#            except:
#                      row1 = ''
#                      row2 = ''
#                      first_ = row1
#                      next_ = row2

#            matrice.append([first_,next_])
#            f.write(string + '\n')



# df = pd.DataFrame(matrice, columns=['TIME', 'WATERLEVEL'])


# matrix_final = np.array(df)
# impute_knn(matrix_final)
# matrix_imputed = imputation_mean(matrix_final)

# df = pd.DataFrame(matrice, columns=['TIME', 'WATERLEVEL'])

# time_list = df['TIME'].tolist()

# new_list = []
# for i in range(0, len(time_list)):
#     if math.isnan(time_list[i]):
#        time_ = time_list[i-1] + 600
#        time_list[i] = time_
#        new_list.append(time_list[i])
#     else:
#        new_list.append(time_list[i])



# print "After imputation: " + str(len(new_list))

# df = pd.DataFrame(matrix_imputed, columns=['TIME', 'WATERLEVEL'])
# list_new = list(dict.fromkeys(new_list))
# df["TIME"] =  list_new
# df.to_csv(r'imputed_merged.csv')
# print(str(new_list))



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