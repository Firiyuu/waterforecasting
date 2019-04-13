from knn import impute_knn
import pandas as pd

data = pd.read_csv("nan1.csv")

data.insert(0, 'TimeframeId', range(0,len(data)))

print data

impute_knn(data)
# matrix_imputed = imputati