# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:43:04 2019

@author: tbernard
"""

import numpy as np
import matplotlib.pyplot as plt

for i in range (4,5):
    if i <10:
        file_number="00" + str(i) 
    elif 10<=i<100:
        file_number = "0"+ str(i)
    else:
        file_number = str(i)


    
    # Load X, Y, Z position data
#    FN1 = "D:/papier M2/Analyses/individual_scar.csv"
#    X = np.loadtxt(FN1,delimiter=';', usecols = 1, skiprows=1)
#    Y = np.loadtxt(FN1,delimiter=';', usecols = 2, skiprows=1)
#    Z = np.loadtxt(FN1,delimiter=';', usecols = 3, skiprows=1)
#    plt.figure(1)
#    plt.plot(X,Y,'k.', markersize=2)
#    xmin, xmax = plt.xlim()
#    ymin, ymax = plt.ylim()
#    plt.xlim(xmin, xmax)
#    plt.ylim(ymin,ymax)
    # Load M3C2 data
    FN = "D:/papier M2/Analyses/individual_scars/individual_scar_000" + file_number + '.txt'
    data = np.loadtxt(FN,delimiter=',', usecols = 12, skiprows=1)
    data=data[data>0]
    bin_size = 0.5; min_edge = np.min(data); max_edge = np.max(data)
    N = (max_edge-min_edge)/bin_size; Nplus1 = N + 1
    bin_list = np.linspace(min_edge, max_edge, Nplus1)
    plt.figure(2)
    plt.hist(data, bins=bin_list, histtype='bar',edgecolor = 'k', linewidth=0.5, density =True, label= 'Scar ' + str(i))
    plt.legend(loc='upper-right')
    ymin, ymax =plt.ylim()
    plt.xlim(0,30)
    plt.ylim(ymin,1)
    plt.xlabel('Height (m)',fontsize = 16, fontweight = 'bold')
    plt.ylabel('probability density',fontsize = 16, fontweight = 'bold')
    plt.show()