from sklearn import preprocessing
from sklearn.preprocessing import Normalizer
import pandas as pd
import numpy as np
import time

     
def normalization(matrix):
   scaled = preprocessing.scale(matrix) #minmax scaling
   print str(scaled)
   normalized = preprocessing.normalize(scaled, norm='l2')
   print str(normalized)
   return normalized



def transform(matrix):

	#ang scaled data kay dili man sya 2D
	# matrix = np.array(matrix)
	df = pd.DataFrame(matrix, columns=['SCALED'])
	matrix = df.reshape(1,268177)
	transformer = Normalizer().fit(matrix) # fit does nothing.
	transformer.transform(matrix)