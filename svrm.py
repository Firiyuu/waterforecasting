from sklearn.svm import SVR
import numpy as np



n_samples, n_features = 10, 5
np.random.seed(0)
y = np.random.randn(n_samples)
X = np.random.randn(n_samples, n_features)
clf = SVR(gamma='scale', C=1.0, epsilon=0.2)
clf.fit(X, y) 


# Only consider rainfaill for SVR forecasting model
# daily histoirical water level data aquired
# Water level and rainfaill

# 10 mins, but around 39 and 40 has 30 mins gap

# Detect which aren't in that gap