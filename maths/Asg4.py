#
#	Assignment 4
#

""" 
TASK 1
"""

from numpy import *
from pylab import *
from splbasis_2 import *

import s1002

# a)

# This function is used in a step for generating a spling out of the data points
# xint and yint. The function generates a vector containing one sigma for each spline
def get_sigma(xint, yint, h):
	# m is the number of splines 
	# len(datapoints) = m+1
	m = len(xint)-1
	# Generate the sigma matrix A that operates on sigma_1 to sigma_m-1
	# sigma_0 = 0 and sigma_m = 0
	A = diag([4]*(m-1)) + diag([1]*(m-2),1) + diag([1]*(m-2),-1)
	# The b-vector for the system Ax = b where x is the vector of sigmas from 1 to m-1
	# is generated below:
	y = []
	for i in range(1,m):
		y.append(6.0/(h**2)*(yint[i+1] - 2*yint[i] + yint[i-1]))
	# res is the vector containing the values of sigma from 1 to m-2
	res = linalg.solve(A,y)
	# filling in zeros for sigma_0 (index) and sigma_m-1 (index) and appending the resulting values for 
	# sigma 1 to m - 1 to generate the final values of all sigmas from 0 to m-1 (index). 
	# The resulting vector is a vector of all the m numbers of sigmas. One for each spline 
	sigma = [0]
	sigma.extend(res)
	sigma.append(0)

	return sigma

def get_a(sigmas,h):
	a = []
	for i in range(len(sigmas)-1):
		a.append((sigmas[i+1] - sigmas[i])/(6.0*h))
	return a

def get_c(yint, sigmas, h):
	c = []
	for i in range(len(sigmas)-1):
		c.append((yint[i+1]-yint[i])/h - (2*sigmas[i] + sigmas[i+1])*h/6.0)
	return c

def cubspline(xint, yint):
	# Assuming equidistant points
	h = xint[1] - xint[0]
	sigmas = get_sigma(xint,yint,h)
	a = get_a(sigmas, h)
	# b_i = sigma_i where i = 0, ... , m-1
	b = copy(sigmas[:-1])/2.0
	c = get_c(yint, sigmas, h)
	# d_i = y_i, the most simple
	d = copy(yint[:-1])

	matrix = []

	for i in range(len(a)):
		matrix.append([])
		matrix[i].append(a[i])
		matrix[i].append(b[i])
		matrix[i].append(c[i])
		matrix[i].append(d[i])

	return matrix

# b)

def cubsplineval(coeff,xint,xval):
	h = xint[1]-xint[0]
	i = int((xval - xint[0])/h)
	if i == len(coeff):
		return polyval(coeff[i-1], (xval-xint[i-1]))
	return polyval(coeff[i],xval-xint[i])

""" 
	TASK 2
"""
# a)

x = range(7)
y = [1,3,-2,0,1,0,1]

coeff = cubspline(x,y)
print coeff
xvals = arange(0,6,0.01)
plot(x,y,'bo')

plot(xvals,[cubsplineval(coeff, x, xval) for xval in xvals], 'r')
#title("Spline of data")
#legend(["Data knots","Spline function"])
#show()
# b) 

xi = [0,0,0]
xi.extend(x)
xi.extend([x[-1]]*3)

# After testing - this was our resulting vector of di! 
di = [1,2.4,5.38,-4.6,1,1.35,-0.7,0.5,1]

dx = 0.01

xvals_test = arange(0,6.001,dx)

yvals_test = Bsplbasis(xi, di, dx)
print "yvals test len: ",len(yvals_test),", xi len:", len(xvals_test)
plot(xvals_test, yvals_test, 'b')
xlabel("X")
ylabel("Y")
title("B-spline interpolation of given data")
legend(["Data points","Cubic spline","Cubic B-spline"])
show()

# m is the number of splines
m = len(y) - 1
# the number n represents the number of basis terms
n = m + 3


points = 50
xdata = linspace(-70, 60, points)
ydata = [-1*s1002.s1002(x) for x in xdata]
plot(xdata, ydata, 'ro')


#plotting the actual wheel
xplot = linspace(-70, 60, 1000)
yplot = [-1*s1002.s1002(x) for x in xplot]
plot(xplot, yplot, 'r')

#b and c
#makes out and prints the splines
figure(2)
coeff = cubspline(xdata, ydata)
xvals = linspace(-70, 60, 1000)
plot(xvals,[cubsplineval(coeff, xdata, xval) for xval in xvals])
title("The wheel with {} interpolation points".format(points))
xlabel("Length / mm")
ylabel("Height / mm")
show()




