import numpy as np
from sklearn.impute import SimpleImputer
import pandas as pd



def imputation_mean(matrix):
    # Inputs are Matrix and np.nan created
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    print(imp.fit(matrix))
    matrix = imp.transform(matrix)
    df = pd.DataFrame(matrix, columns=['TIME', 'WATERLEVEL'])
    df.to_csv(r'imputed.csv')
    print "Written to CSV"
    return matrix


def imputation_k(matrix):
    imp = SimpleImputer(missing_values=np.nan, strategy='knn')
    print(imp.fit(matrix))
    matrix = imp.transform(matrix)
    df = pd.DataFrame(matrix, columns=['TIME', 'WATERLEVEL'])
    df.to_csv(r'imputed.csv')