# -*- coding: utf-8 -*-
"""
Created on Sat May 11 14:59:09 2019

@author: tbernard
"""
import numpy as np
import numpy.random
from scipy import log
from scipy.special import zeta
from scipy.optimize import bisect 
from scipy import sqrt

from scipy import stats
from scipy.optimize import minimize, leastsq

def MLE_fit(X,Y):
   # X = np.log(X)
    Y = np.log(Y)
    def power(params):
        a  = params[0]
        b  = params[1]  
        sd = params[2] 

        yPred = np.log(a)+b*np.log(X)

        # Calculate negative log likelihood
        LL = -np.sum( stats.norm.logpdf( Y , loc=yPred, scale=sd ) )
           
        return(LL)    
    
    
    initParams = [1, 1, 1]

    results = minimize(power, initParams, method='Nelder-Mead',options={'maxiter':100000})
    print('Results of MLE fit are:')
    print(results.x)

    estParms = results.x
    yOut = yPred = np.log(estParms[0])+estParms[1]*np.log(X)
        
    # results
    a = np.around(results.x[0],3)
    b = np.around(results.x[1],4)
    sd = np.around(results.x[2],4)
    
    
    return a, b, sd    

def weighted_linear_fit(X,Y,sigma):
    variance = (sigma**2)/(Y**2)
    weight = 1/variance
    p, v = np.polyfit(X,Y,deg=1,w=weight,cov='unscaled')
    std = np.sqrt(np.diag(v))
    print(p, std)
    return p, v, std

def linear_fit_v1(X,Y):
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(X), np.log10(Y))
    print('['+str(intercept)+','+str(slope)+']'+ ' ['+str(std_err)+','+str(p_value)+']')
    return slope, intercept, r_value, p_value, std_err

def linear_fit(X,Y,sigma,weight):
    X = X
    Y = Y
    def func(x,c1,c2):
        return c1 + c2*x
    guess = [0.5,2]
    nX = len(X)
    y = np.empty(nX)
    for i in range(nX):
        y[i] = func(X[i],guess[0],guess[1])

    from scipy.optimize import curve_fit
    if weight==1:
        variance = (np.log10(sigma)**2)/(np.log10(Y)**2)
        weight = 1/variance
        cl, covl = curve_fit(func,np.log10(X),np.log10(Y),guess,method ='lm',maxfev=10000,sigma=np.log10(sigma),absolute_sigma=True)
    else:
        cl, covl = curve_fit(func,np.log10(X),np.log10(Y),guess,method ='lm',maxfev=10000)
        
    stdl = np.sqrt(np.diag(covl))
    print(cl , stdl )
    y_est= 10**cl[0]*X**cl[1]

    # estimate r²
    from sklearn.metrics import r2_score
    R = r2_score(np.log10(Y),np.log10(y_est))
    print('R² = ', r2_score(Y,y_est))
    
    return cl, stdl, R, y_est   

def density_plot2D( x , y, ax = None, sort = True, bins = 60, **kwargs )   :
    """
    Scatter plot colored by 2d histogram
    """
    from scipy.stats import gaussian_kde
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.interpolate import interpn
    from matplotlib.gridspec import GridSpec
    
    fig = plt.figure()
    gs = GridSpec(4,4)
    data , x_e, y_e = np.histogram2d( x, y, bins = bins, density=True)
    z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , np.vstack([x,y]).T , method = "splinef2d", bounds_error = False )
    
    ax_joint = fig.add_subplot(gs[1:4,0:3])
    ax_marg_x = fig.add_subplot(gs[0,0:3])
    ax_marg_y = fig.add_subplot(gs[1:4,3])
    #ax_colorbar.axis('off')
    
    scatter=ax_joint.scatter( x, y, c=z,s=1, **kwargs )
    hist_x=ax_marg_x.hist(x,bins=300, density=True)
    hist_y=ax_marg_y.hist(y,orientation="horizontal",bins=300,density=True)
    #fig.colorbar(z)
    # Turn off tick labels on marginals
    plt.setp(ax_marg_x.get_xticklabels(), visible=False)
    plt.setp(ax_marg_y.get_yticklabels(), visible=False)

    

    # Sort the points by density, so that the densest points are plotted last
    if sort :
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]
    
    
    #legend
    #cbar.set_label( 'Nb of points in each bin', rotation=270,labelpad=20, fontweight='bold')
    
     # Set labels on joint
    ax_joint.set_xlabel('')
    ax_joint.set_ylabel('')

    # Set labels on marginals
    ax_marg_y.set_xlabel('')
    ax_marg_x.set_ylabel('')

    plt.show()
    return ax
