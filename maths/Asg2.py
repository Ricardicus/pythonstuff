# Assignment 2
#
#	Task 1
#
#
from math import *
import scipy
from scipy.linalg import *
from pylab import *

def F(x):
	alpha = x[0]
	beta = x[1]
	F1 = 5*cos(alpha) + 6*cos(alpha+beta) - 10
	F2 = 5*sin(alpha) + 6*sin(alpha+beta) - 4
	return array([F1,F2])

def analytical_jac(x):
	alpha = x[0]
	beta = x[1]
	R1C1 = -5*sin(alpha) - 6*sin(alpha)
	R1C2 = -6*sin(alpha+beta)
	R2C1 = 5*cos(alpha) + 6*cos(alpha+beta)
	R2C2 = 6*cos(alpha+beta)
	return array([[R1C1,R1C2],[R2C1,R2C2]])

def newton(f,guess,iterations=1000):
	# newton, add tolerance later?
	x = guess 
	results = []
	for n in range(iterations):
		x = x - dot(inv(analytical_jac(x)),F(x))
		results.append(x)	
	return x, results

#ans, results = newton(F,[0.7,0.7],100)
#for i in results:
#	print i
#print F(ans)

#
# Task 2
#

# a)

def create_A(alpha=1):
	#a = [[0]*30]*30
	a = array(zeros((30,30)))
	a[0][0] = -(2+alpha)
	a[0][1] = 1
	a[-1][-1] = -(2+alpha)
	a[-1][-2] = 1
	for j in range(1,29):
		a[j][j] = -(2+alpha)
		a[j][j-1] = 1
		a[j][j+1] = 1
	return a

def create_b():
	b = array(zeros(30))
	b[5] = 2
	return b

def factor_LU(x):
	L = array(eye(len(x)))
	U = x
	count = 0
	for n in range(0,len(x)):
		for j in range(n+1,len(x)):
			if(U[n][n] != 0):
				k = U[j][n] / U[n][n]
				U[j] = U[j] - k * U[n]
				L[j][n] = k
				count+=1
			else:
				L[j][n] = 0
	return L,U,count

A = create_A()
L,U,count_LU = factor_LU(create_A())
b = create_b()

# the dot product of a nxn matrix and a n-vector requires n^2 operations in general.
y = dot(inv(L),b)
count_LU += len(L)**2

# the dot product of a nxn matrix and a n-vector requires n^2 operations in general.
x_exakt = dot(inv(U),y)
count_LU += len(U)**2

# returns vector b (the system equation is satisfied)
print x_exakt

# ------> b) <-------

# to create the Jacobi-G matrix in the iterative scheme
def create_G_C_jacobi():
	b = create_b()
	A = create_A()
	Q = array(eye(len(A)))
	count = 0
	for j in range(30):
		Q[j][j] = A[j][j]
	Q_inv = array(eye(len(A)))
	for j in range(30):
		# knowing that Q[j][j] never is zero
		Q_inv[j][j] = 1/Q[j][j]
		count+=1
	# Dot product of two nxn-matrices require n^3 multiplications.
	# Is this wrong to assume? We suspect that it can be less due to the many zeros
	# in the matrix.
	G = eye(30) - dot(Q_inv,A)
	count += len(Q_inv)**3
	
	# Dot product of one nxn-matrix and a n-vector requre n^2 multiplications.
	# Is this wrong to assume? We suspect that it can be less due to the many zeros
	# in the matrix.
	C = dot(Q_inv,b)
	count += len(Q_inv)**2

	return G, C, count

def Q_inverse_Gauss_Seidel(Q):
#	A = create_A()
#	b = create_b()

# A is the triangular matrix now that should be inversed
	A = Q.copy()
	operation_count = 0
	A_inv = array(eye(len(Q)))
	for j in range(len(Q)):
		for i in range(j+1,len(Q)):
		# knowing that the diagonals are never zero
			A_inv[i] = A_inv[i] - (float(A[i][j])/float(A[j][j]))*A_inv[j]
			operation_count+=len(A_inv[j])*2
			A[i] = A[i] - (float(A[i][j])/float(A[j][j])) * A[j]
			operation_count+=len(A[j])*2
	for j in range(len(A)):
		# knowing that the diagonals are never zero
		A_inv[j] = (1/float(A[j][j]))*A_inv[j]
		operation_count+=len(A[j])*2
		A[j] = (1/float(A[j][j]))*A[j]
		operation_count+=len(A[j])*2
	return A_inv,operation_count

def create_G_C_Gauss_Seidel():
	# Q = L + D, start with A and write zeros
	Q = create_A()
	for r in range(len(Q)):
		for c in range(r+1,len(Q)):
			Q[r][c] = 0
	Q_inv, count = Q_inverse_Gauss_Seidel(Q)

	A = create_A()
	b = create_b()

	G = eye(len(A))-dot(Q_inv,A)

	# Dot product of two nxn-matrices require n^3 multiplications
	count += len(A)**3

	# Dot product of one nxn-matrix and a n-vector requre n^2 multiplications
	C = dot(Q_inv,b)
	count += len(A)**2

	return G,C,count

def one_norm(x):
	rows = len(x)
	sum_rows = 0
	for r in range(rows):
		sum_rows+=abs(x[r])
	return sum_rows

def Jacobi_iteration(x0,tolerance=1e-5, iterations=1000):
	G, C, count = create_G_C_jacobi()
	x = x0.copy()
	iteration_history = []
	for i in range(iterations):
		x = dot(G,x) + C
		# we estimate that the dot product between a nxn-matrix and a n-vector 
		# require n**2 operations. Is this wrong to assume?
		count += len(G)**2
		norm = one_norm(x-x_exakt)
		iteration_history.append(norm)
		if(norm<tolerance):
			return x, "success",iteration_history,count
	return x, "fail",iteration_history,count

def Gauss_Seidel_iteration(x0,tolerance=1e-5,iterations=1000):
	G, C, count = create_G_C_Gauss_Seidel()
	x = x0.copy()
	iteration_history = []
	for i in range(iterations):
		x = dot(G,x) + C
		# we estimate that the dot product between a nxn-matrix and a n-vector 
		# require n**2 operations. Is this wrong to assume?
		count += len(G)**2
		norm = one_norm(x-x_exakt)
		iteration_history.append(norm)
		if(norm<tolerance):
			return x, "success", iteration_history,count
	return x,"fail",iteration_history,count

# Can Jacobi or Gauss-Seidel only converge mutually? 
# Whether or not the iterative scheme converges depends solely on the value of the spectral radius 
# of the matrix G. This needs to be less than one to converge. Since G differs in the two schemes one 
# can not be certain that both succeed when only one of the two does. 

#  Iteration history
# ------> c) <-------

# where should we start? 
x_initial = array([0]*30)
figure(1)
iteration_Jacobi = Jacobi_iteration(x_initial)[2]
iteration_Gauss_Seidel = Gauss_Seidel_iteration(x_initial)[2]
plot(iteration_Jacobi,'r-o',iteration_Gauss_Seidel,'b-o')
title("Iteration schemes")
legend(["Jacobi","Gauss-Seidel"])
ylabel("||x_n - x_exact||")
xlabel("Number of iterations ({} Jacobi, {} Gauss-Seidel)".format(len(iteration_Jacobi),len(iteration_Gauss_Seidel)))
show()

# Number of operations * and /
# -------> d) <-------

print "Jacobi count: ",Jacobi_iteration(x_initial)[3]
print "Gauss-Seidel count: ",Gauss_Seidel_iteration(x_initial)[3]
print "LU-factorisation count", count_LU

# Discussion of which method to prefer and why.
# Considering the number of operations required for LU-factorisation, it seem to be the best 
# method for solving this problem. 

G_jacobi, C_jacobi, count_jacobi = create_G_C_jacobi()
G_gauss_seidel, C_gauss_seidel, count_gauss_seidel = create_G_C_Gauss_Seidel()

n = 30
tol = 1e-5

print "Jacobi condition better than Gaussian methods: ", log(tol)/log(max(abs(linalg.eigvals(G_jacobi))))
print "Gauss-Seidel condition better than Gaussian methods: ", log(tol)/log(max(abs(linalg.eigvals(G_gauss_seidel))))

A = array([[1, 2, 2],[1,2,2],[1,1,1]])
L,U,count = factor_LU(A)
print "L: {}\n U: {}".format(L, U)

