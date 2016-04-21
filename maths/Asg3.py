#
# Assignment 3
#

# TASK 1

from numpy import * 
from pylab import *
from math import *

# a)

def my_polyval(coeffs, x):
	sum = 0
	for i in range(len(coeffs)):
		sum+=coeffs[i]*x**(len(coeffs)-1-i)
	return sum

def get_vandermonde_coeffs(xvals, yvals):
	
	n = len(xvals)
	Vandermonde_matrix = []
	for i in range(n):
		Vandermonde_matrix.append([])
	for i in range(n):
		for k in range(n):
			Vandermonde_matrix[i].append(xvals[i]**(n-1-k)) 
	Vander_coeffs = linalg.solve(Vandermonde_matrix, yvals)

#	print "Conditional number: ",linalg.cond(Vandermonde_matrix)

	return Vander_coeffs

# Plotting using polyfit and polyval
days = array([4,6,8,10,12])
values = array([53.26, 58.83, 53.45, 43.06, 47.7])

coeff = polyfit(days, values, len(days)-1)

plot_april_days = arange(1,15,0.01)
plot_energi = array([polyval(coeff, x) for x in plot_april_days])

plot(plot_april_days, plot_energi)
xlabel("Days in april")
ylabel("Energy")
title("Plot using polyfit and polyval")
show()

print "dag 4: ", polyval(coeff,4)
print "dag 6: ", polyval(coeff,6)
print "dag 8: ", polyval(coeff,8)
print "dag 10: ", polyval(coeff,10)

# Plotting using Vandermonde's approach

Vander_coeffs = get_vandermonde_coeffs(days, values)

print "polyfit: ", coeff
print "Vandermonde: ", Vander_coeffs

print "dag 4: ", my_polyval(Vander_coeffs, 4)

plot_energi = array([my_polyval(Vander_coeffs, x) for x in plot_april_days])

plot(plot_april_days, plot_energi)
xlabel("Days in april")
ylabel("Energy")
title("Plot using our functions get_vandermonde_coeffs and my_polyval")
show()

# b)

print "April 14: ", my_polyval(Vander_coeffs,14), " kwh."

# c) 

old = my_polyval(Vander_coeffs,14)

old_val_two = values[2]
values[2] = values[2]*1.1

Vander_coeffs = get_vandermonde_coeffs(days, values)

new = my_polyval(Vander_coeffs,14)

numerator = (new - old)/max(new,old)
denominator = (values[2] - old_val_two) / max(values[2],old_val_two)
sensitivity = numerator / denominator

print "sensitivity: ", sensitivity

# TASK 2

def w(points,x):
	product = 1
	for p in points:
		product*=abs(x-p)
	return product

points_one = arange(-1,1.1,2.0/4)
points_two = sort([-1 + rand() for x in range(5)])
points_three = sort([1 - rand() for x in range(5)])

xvals = arange(-1,1,0.001)

plot(xvals,[w(points_one,x) for x in xvals],'r', points_one, [0]*5, 'bo')
show()

plot(xvals,[w(points_two,x) for x in xvals],'r', points_two, [0]*5, 'bo')
show()

plot(xvals,[w(points_three,x) for x in xvals],'r', points_three, [0]*5, 'bo')
show()

# optimal after tesing with n = 5 was points_one ie. equidistant points 
# testing interpolation points with n = 15

points_one = arange(-1,1.1,2.0/14)
points_two = sort([-1 + rand() for x in range(15)])
points_three = sort([1 - rand() for x in range(15)])

plot(xvals,[w(points_one,x) for x in xvals], 'r', points_one, [0]*15, 'bo')
show()

# Finding the maximum error
print max([w(points_one,x) for x in xvals])

plot(xvals,[w(points_two,x) for x in xvals], 'r', points_two,[0]*15, 'bo')
show() 

plot(xvals,[w(points_three,x) for x in xvals], 'r', points_three, [0]*15, 'bo')
show()

# Once again, we think that equidistant points give the most satisfying result 
# but we know that Chebyshev points is optimal

# TASK 3

# Chebyshev points for n = 15 are the roots to the Chebyshev polynomial of degree 15. 

def get_chebyshev_points(n):
	points = []
	for k in range(1,n+1):
		points.append(cos((2.0*k-1)/(2*n)*pi))
	return sort(points)

points = get_chebyshev_points(15)

plot(xvals,[w(points,x) for x in xvals], 'r', points,[0]*15, 'bo')
#xlabel("Interpolation points: {}".format(points_two))show()
show() 

print max([w(points,x) for x in xvals])

# We see that this was optimal! 

# TASK 4

# a) 

def f(x):
	return 1.0/(1+25*x**2)

# with n = 3
three_points = arange(-1,1.1,2.0/2)
xvalues = arange(-1,1,0.0001)

Vander_coeffs = get_vandermonde_coeffs(three_points, [f(x) for x in three_points])
yvals_three = [my_polyval(Vander_coeffs, x) for x in xvalues]

# with n = 9
nine_points = arange(-1,1.01, 2.0/8)

Vander_coeffs = get_vandermonde_coeffs(nine_points, [f(x) for x in nine_points])
yvals_nine = [my_polyval(Vander_coeffs, x) for x in xvalues]

# with n = 15
fifteen_points = arange(-1,1.01, 2.0/14)

Vander_coeffs = get_vandermonde_coeffs(fifteen_points, [f(x) for x in fifteen_points])
yvals_fifteen = [my_polyval(Vander_coeffs, x) for x in xvalues]

figure(1)
plot(xvalues, yvals_three, 'r', xvalues, yvals_nine, 'b', xvalues, yvals_fifteen, 'g', xvalues, [f(x) for x in xvalues], 'k')
legend(["n=3", "n=9", "n=15", "f(x)"])
title("Interpolation of f(x)")
show()

diff_three = []
i = 0
for x in xvalues:
	diff_three.append(abs(yvals_three[i]-f(x)))
	i+=1

diff_nine = []
i = 0
for x in xvalues:
	diff_nine.append(abs(yvals_nine[i]-f(x)))
	i+=1

diff_fifteen = []
i = 0
for x in xvalues:
	diff_fifteen.append(abs(yvals_fifteen[i]-f(x)))
	i+=1

plot(xvalues, diff_three, 'r', xvalues, diff_nine, 'b', xvalues, diff_fifteen, 'g')
legend(["n=3", "n=9", "n=15", "f(x)"])
title("Interpolation error of f(x)")
show()

# b)

# doing the above with Chebyshev points: 

# with n = 3
three_points = get_chebyshev_points(3)

xvalues = arange(-1,1,0.0001)

Vander_coeffs = get_vandermonde_coeffs(three_points, [f(x) for x in three_points])
yvals_three = [my_polyval(Vander_coeffs, x) for x in xvalues]

# with n = 9
nine_points = get_chebyshev_points(9)

Vander_coeffs = get_vandermonde_coeffs(nine_points, [f(x) for x in nine_points])
yvals_nine = [my_polyval(Vander_coeffs, x) for x in xvalues]

# with n = 15
fifteen_points = get_chebyshev_points(15)

Vander_coeffs = get_vandermonde_coeffs(fifteen_points, [f(x) for x in fifteen_points])
yvals_fifteen = [my_polyval(Vander_coeffs, x) for x in xvalues]

figure(2)

plot(xvalues, yvals_three, 'r', xvalues, yvals_nine, 'b', xvalues, yvals_fifteen, 'g', xvalues, [f(x) for x in xvalues], 'k')
legend(["n=3", "n=9", "n=15", "f(x)"])
title("Interpolation of f(x) with Chebyshev points")
show()

diff_three = []
i = 0
for x in xvalues:
	diff_three.append(abs(yvals_three[i]-f(x)))
	i+=1

diff_nine = []
i = 0
for x in xvalues:
	diff_nine.append(abs(yvals_nine[i]-f(x)))
	i+=1

diff_fifteen = []
i = 0
for x in xvalues:
	diff_fifteen.append(abs(yvals_fifteen[i]-f(x)))
	i+=1

plot(xvalues, diff_three, 'r', xvalues, diff_nine, 'b', xvalues, diff_fifteen, 'g')
legend(["n=3", "n=9", "n=15", "f(x)"])
title("Interpolation error of f(x)")
show()


# TASK 5



