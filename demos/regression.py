# taken from https://machinelearningmastery.com/solve-linear-regression-using-linear-algebra/
# solve directly
from numpy import array
from numpy.linalg import inv
from matplotlib import pyplot
import mpld3

data = array([
	[0.05, 0.12],
	[0.18, 0.22],
	[0.31, 0.35],
	[0.42, 0.38],
	[0.5, 0.49],
	])
X, y = data[:,0], data[:,1]
X = X.reshape((len(X), 1))
# linear least squares
b = inv(X.T.dot(X)).dot(X.T).dot(y)
print(b)
# predict using coefficients
yhat = X.dot(b)
# plot data and predictions
pyplot.scatter(X, y)
pyplot.plot(X, yhat, color='red')
mpld3.show()
