from math import *
import sys

import numpy as np

def likelihood(b0, sigmab, nobs, s0, sigmas, randomseed = 0):

    if randomseed != 0:
      np.random.seed(randomseed)

    n_BkgSig = b0 + s0
    err_BkgSig = sqrt(sigmab*sigmab + sigmas*sigmas)    
    
    # Use Gaussian approximation if predicted number of events greater than 20
    if(n_BkgSig > 30):
	sig2 = (pow(nobs - n_BkgSig, 2))/(nobs + (err_BkgSig*err_BkgSig))
    
    # For low statistics use gaussian convoluted with gaussian
    else:
	distListSig = []
	distList = []
	nb = 0
	nsb = 0
	ntot = 100000
	bkgSigList = np.random.normal(n_BkgSig,err_BkgSig,ntot)
#    	obslist = np.random.normal(Nobs,errNbkg,ntot)
	for i in range(0,ntot):
	    distListSig.append(np.random.poisson(max(0.000001,bkgSigList[i])))
	    distList.append(np.random.poisson(max(0.000001,nobs)))
	    if distList[i]==nobs:
		nb=nb+1
	    if distListSig[i]==nobs:
		nsb=nsb+1
	cls=float(nsb)/nb
	sig2 = -2.*log(cls)
    
    return(sig2)
    
