"""
TASK 2 b)
"""
from numpy import *
from pylab import *
from math import *

#Task 2

#this function approximates the value of the integral of f(x)
#in the interval [a,b] using the Simpson composite rule with n steps
def composite_simpson(f, n, a, b):
	h = (b-a)/(n*1.0)
	return h/6*(f(a) + 4*f(a+h/2) + sum([2*f(xj)+4*f(xj+h/2) for xj in add(a,multiply(h,range(1, n)))]) + f(b))

q = 5.0
print composite_simpson(lambda x: x**(q-1),3,0,10)
print 10**q/q

# Works for x**3 but for x**4 the value doesn't converge to the correct one

#this function approximates the value of the integral of f(x)
#in the interval [a,b] using three point composite Gauss rule with n steps
def three_point_composite_gauss(f,n,a,b):
	
	h = (b-a)/(n*1.0)
	return h/18.0*sum( [ 5*f(x + ((5-sqrt(15))/10.0)*h) + 8*f(x+(5.0/10)*h) + 5*f(x+(5+sqrt(15))*h/10.0) for x in arange(a,b,h)] )

q = 6.0
print three_point_composite_gauss(lambda x: x**(q-1),3,0,10)
print 10**q/q

# Works for x**5 but for x**6 the value doesn't converge to the correct one

#print three_point_composite_gauss(cos,3,0,pi)

"""
TASK 3
"""

# a)

# fourth derivative of the function:
def f(x):
	return 96.0*(5*x**4 - 10*x**2 + 1)/((1+x**2)**5)

xvals = arange(0,1,0.001)
plot(xvals,[f(x) for x in xvals])
title("f''''(x)")
show()

# knowing that this reaches 96 at maximum the maximum possible error can be calculated
# the condition for n is then derived to be:
# n >= 14

# b)

print "Composite Gauss: ",three_point_composite_gauss(lambda x: 4/(1+x**2),14,0,1) - pi
print "Composite Simpsons: ",composite_simpson(lambda x: 4/(1+x**2),14,0,1) - pi

# The results were very good. We are suprised to see that the maximum value of the error codition (10^-6)
# was many orders of magnitude bigger than the actual error we got by computing with the condition n = 14.
# Can this be explained by assuming that the maximum error not necessarily have to be close to the actual computed error?

print "integral of complicated function [simpsons]: ",three_point_composite_gauss(lambda x: exp(x) - sin(x) + atan(0.2*x), 4, -1,1)


"""
TASK 4
"""

# a)
# Yes we need one extra grid point on each side. If we don't have one extra at each end we will not satisfy the condition that the sum of 
# all basis-functions for each x-value should equal one. It is sufficient with one extra grid point on each side since any basis functions
# further out than that will not have a non-zero valeu within the interpolation interval.

# Yes we need one extra grid point for the construction grid on each side of the interval. This is needed to ensure that the sum of 
# all basis for every x is 1. 

# b) on paper

# c) 
def window(a, b, x):
	if x < b and x >= a:
		return 1
	return 0

def N02(x):
	return (1-x)*window(0,1,x)

def N12(x):
	return x*window(0,1,x) + (2-x)*window(1,2,x)

def N22(x):
	return (x-1)*window(1,2,x) + (3-x)*window(2,3,x)

def N32(x):
	return (x-2)*window(2,3,x)

xvals = arange(0,3, 0.01)
plot(xvals, [N02(x) for x in xvals], 'r', xvals, [N12(x) for x in xvals], 'b', xvals, [N22(x) for x in xvals], 'g', xvals, [N32(x) for x in xvals], 'k')
legend(["N_02(x)", "N_12(x)","N_22(x)", "N_32(x)"])
title("B-spline basis polynomials")
show()

# estimation of areas
print("Area under N02: ", three_point_composite_gauss(N02,10,0,3))
print("Area under N12: ", three_point_composite_gauss(N12,10,0,3))
print("Area under N22: ", three_point_composite_gauss(N22,10,0,3))
print("Area under N32: ", three_point_composite_gauss(N32,10,0,3))


