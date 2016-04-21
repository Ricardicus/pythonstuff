# -*- coding: utf-8 -*-
"""
@author: Alex
"""
from scipy import *
from matplotlib.pyplot import *

def Bsplbasis(xi,di,dx):
    """
    This algorithm will evaluate the N_{i,4} at specific range given by the xi input.
    
    On input:
    =========
    xi.... List or array. Length=m+7. xi is composed of m+1 knots 
           and 6 additional points: 3 points on either side of the boundary. 
           Preferably repeat the first and last knot in the input list xi.
    di.... List or array of the m+3 de Boor points --- THIS IS WHAT YOU ARE SUPPOSED TO FIND
    dx.... Float number such as for instance .01 (or similar) which is used in terms 
           of how fine to plot the resulting spline curve
    On return:
    ==========
    q..... List containing the computed values of the spline at points in range of xi.
           Specifically at xi[3]+i*dt, i=0,... as long as xi[3]+i*dt <= xi[-4]  
    """
    eps = 1.e-14
    m = len(xi) 
    i = 4      #index of first knot
    q=[]
    for u in arange(xi[3],xi[m-3]+dx,dx):
        # check if u value has moved to the next knot interval
        # include small tolerance on knots to avoid round-off error in comparisons.
        
        while (u>(xi[i]+eps)):
            i+=1
        # Now evaluate the spline at u using the deBoor algorithm.
        # Start with the relevant control points.
        im4 = i-4
        qq = zeros(len(di))
        for j in range(1,5,1):
            qq[j-1]=di[im4+j-1]
        for j in range(1,4,1):
            for k in range(1,4-j+1,1):
                qq[k-1] = ((xi[im4 + k + 4-1] - u)/(xi[im4 + k + 4-1] - xi[im4 + k + j-1])) * qq[k-1] + \
                            ((u - xi[im4 + k + j-1])/(xi[im4 + k + 4-1] - xi[im4 + k + j-1])) * qq[k+1-1]
        #Create list of points on the B-spline curve.
        q.append(qq[0])
    return q