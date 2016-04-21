from numpy import *
from pylab import *
import s1002
from Asg4 import *

#Task 3 assignment 4

#a)
#picking interpolation points and generating data
figure(3)
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
coeff = cubspline(xdata, ydata)
xvals = linspace(-70, 60, 1000)
plot(xvals,[cubsplineval(coeff, xdata, xval) for xval in xvals])
title("The wheel with {} interpolation points".format(points))
xlabel("Length / mm")
ylabel("Height / mm")
legend(["Knots", "Actual wheel function", "Spline of wheel function"], loc=4)
show()