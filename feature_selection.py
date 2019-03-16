from sklearn.feature_selection import VarianceThreshold



def feature_selection(matrix):
   sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
   data_prepared = sel.fit_transform(matrix)
   df = pd.DataFrame(data_prepared, columns=['TIME', 'WATERLEVEL'])
   df.to_csv(r'prepared.csv')

