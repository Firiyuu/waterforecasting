import numpy as np
from sklearn.impute import SimpleImputer




def imputation(matrix):
	# Inputs are Matrix and np.nan created
    imp = SimpleImputer(missing_values='NaN', strategy='mean')
    imp.fit(matrix) #matrix
    print(imp.transform(matrix))
          
