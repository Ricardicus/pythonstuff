import math
def DFT(v):
	N = len(v)
	k_v = []
	for k in range(N):
		sum = 0.0 + 0.0j
		for n in range(N):
			sum+=v[n]*math.e**(-1j*2*math.pi*k/N*n)	
		k_v.append(sum)
	return k_v
def IDFT(v):
	N = len(v)
	n_v = []
	for n in range(N):
		sum = 0.0 + 0.0j
		for k in range(N):
			sum+=v[k]*math.e**(1j*2*math.pi*k/N*n)
		n_v.append(sum/N)
	return n_v