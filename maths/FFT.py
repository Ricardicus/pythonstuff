import math
from Tkinter import *
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
def plot(y):
	master = Tk()
	width = 600
	height = 300
	w = Canvas(master, width=width, height=height)
	w.pack()
	for i in range(len(y)):
		w.create_rectangle(i*width/len(y),height-y[i]*(height-5)/(max(y)-min(y)),(i+1)*width/len(y),height, fill="blue")
