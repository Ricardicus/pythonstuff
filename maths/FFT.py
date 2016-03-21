import math
def DFT(v):
	N = len(v)
	k_v = []
	for k in range(N):
		sum = 0.0 + 0.0j
		for n in range(N):
			sum+=v[n]*math.e**(-1j*2*math.pi*k/N*n)	
		sum = float("{0:.4f}".format(sum.real)) + 1j*float("{0:.4f}".format(sum.imag))
		k_v.append(sum)
	return k_v
def IDFT(v):
	N = len(v)
	n_v = []
	for n in range(N):
		sum = 0.0 + 0.0j
		for k in range(N):
			sum+=v[k]*math.e**(1j*2*math.pi*k/N*n)
		sum = float("{0:.4f}".format(sum.real)) + 1j*float("{0:.4f}".format(sum.imag))
		n_v.append(sum/N)
	return n_v