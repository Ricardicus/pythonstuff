from pylab import * 

#
# TASK 1
# By Rickard Hallerback
# This program is written in Python v. 2.6 
# 

# a)
def plot_function(f,a,b):
	array = arange(a,b,0.001)
	values = []
	for i in array:
		values.append(f(i))
	plot(array,values)
	show()

# b)
def bisec(f,a,b,tol,iteration_history=False,title="Bisection iteration history"):
	a_initial,b_initial,roots_array,x_root_differences = a,b,[],[]
	a = float(a)
	b = float(b)
	if(b<a):
		print "Error: Upper limit in interval was less than lower limit"
		raise Exception("Error", "Interval error")
	root = 0
	for i in range(10000):
		root = (a+b)/2	
		dif = b - root

		if(iteration_history):
			roots_array.append(root)
			x_root_differences.append(dif)

		if((f(a)*f(root)).__lt__(0.0)):
			b = root
		else:
			a = root
		if(dif < tol and (f(a)*f(b)).__lt__(0.0)):
			if(iteration_history):
				history_plot(f,a_initial,b_initial,roots_array,x_root_differences,title)
			return root
	print "OBS: The root was not found within the given level of tolerance"
	raise Exception("Error", "Root not found", root)
# c)
def f(x):
	return x.__pow__(2) - 2

#
# TASK 2
# 

from scipy.optimize import fsolve

# It gives us the answer sqrt(2)
print "fsolve: ",fsolve(f,0.1)

#
# TASK 3
#

# a) If and only if g(x) = x when f(x) = 0 and |g'(x)| < 1
# will the algorithm work. The given function g(x) = x(x^2+6)/(3x^2+2)
# which gives us the derivative g'(x) = 3(x^2-2)^2/(3x^2+2)^2 throgh some
# analytical analysis (product rule ect..). 
# Plotting the derivative g'(x) gives us a function that reaches 1/3 for values reaching
# negative and positive infinity and 3 for x = 0. 
# This iteration method will therefore only converge in specific intervals.
# b) This method is called a fixed point iteration method.

# c) 
# this is the function g(x):
def g(x):
	x = float(x)
	return x*(x.__pow__(2)+6)/(3*x.__pow__(2)+2)
# this is the FPI function
def fpi(function,x0,tolerace,iteration_history=False,title="Fixed point iteration history"):
	nbr_of_iterations = 1000
	x = float(x0)

	xmin,xmax,x_roots,x_root_differences = x0,x0,[],[]

	for i in range(nbr_of_iterations):
		xold = x
		x = function(x)
		if(x<xmin):
			xmin = x
		if(x>xmax):
			xmax = x
		x_roots.append(x)
		x_root_differences.append((x-xold).__abs__())
		if((x-xold).__abs__().__lt__(tolerace)):
			if(iteration_history):
				history_plot(function,xmin-1,xmax,x_roots,x_root_differences,title)
			return x
	raise Exception("Error", "Could not find root with given level of tolerance")

# 
# TASK 4
#

# This is the newton method
def newton(function, x0, tolerance,iteration_history=False,title="Newton iteration history"):
	h = 0.0001
	nbr_of_iterations = 1000
	x = float(x0)

	xmin,xmax = x0,x0
	x_roots = []
	x_root_differences = []

	for i in range(nbr_of_iterations):
		xold = x
		if(xold<xmin):
			xmin = xold
		if(xold>xmax):
			xmax = xold
		x = x - function(x)*h/(function(x+h)-function(x))
		x_roots.append(x)
		x_root_differences.append(float(xold-x).__abs__())
		if(float(xold-x).__abs__().__lt__(tolerance)):
			if(iteration_history):
				history_plot(function,xmin,xmax,x_roots,x_root_differences,title)
			return x

	raise Exception("Error", "Could not find root with given level of tolerance")

# This is the secant method
def secant(function, x0,x1, tolerance,iteration_history=False,title="Secant iteration history"):

	x0_initial = x0
	x1_initial = x1

	x0 = float(x0)
	x1 = float(x1)

	nbr_of_iterations = 1000

	roots_array = []
	x_root_differences = []

	for i in range(nbr_of_iterations):
		tmp = x1
		try:
			x1 = x0 - function(x0)*(x1-x0)/(function(x1)-function(x0))
		except ZeroDivisionError:
			print "Error: please choose a more appropriate interval for this metod."
		roots_array.append(x1)
		x0 = tmp
		x_root_differences.append(float(x1-x0).__abs__())
		if(float(x1-x0).__abs__().__lt__(tolerance)):
			if(iteration_history):
				history_plot(function,x0_initial,x1_initial,roots_array,x_root_differences,title)
			return x1
	raise Exception("Error", "Could not find root with given level of tolerance")

#
# TASK 5
#

figure_nbr_plot = 1

def history_plot(function,x0,x1,x_roots,x_root_increment,ttl="Iteration history"):

		global figure_nbr_plot
		# to make to plot look a bit cooler
		xkcd()

		figure(figure_nbr_plot,(10,8))
		subplot(211)
		title(ttl)

		x_array = arange(x0,x1,0.0001)
		y_array = []
		for i in x_array:
			y_array.append(function(i))

		y_array_roots = []
		for i in x_roots:
			y_array_roots.append(function(i))

		plot(x_array,y_array,'r',x_roots,y_array_roots,"bo")
	#	axis([x0,x1,min(y_array),max(y_array)])

		ylabel("Function value")
		xlabel("Root iterations")

		axes = subplot(212)
		axes.get_xaxis().set_major_locator(MaxNLocator(integer=True))
		plot(x_root_increment,'bo')
		ylabel("Difference |x_n+1 - x_n|")
		xlabel("Iterations")
		show()

		figure_nbr_plot+=1

print "secant: ",secant(f,1,2,1e-14,True,"Secant iteration")
print "newton: ",newton(f,0.2,1e-14,True,"Newton iteration")
print "bisec: ",bisec(f,0,10,1e-14,True,"Bisection iteration")
print "fpi: ",fpi(g,4,1e-14,True,"Fixed point iteration")




