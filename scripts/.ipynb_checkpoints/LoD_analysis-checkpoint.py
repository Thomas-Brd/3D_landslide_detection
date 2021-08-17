# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 14:43:04 2019

@author: tbernard
"""
import subprocess
#import scripts.cloudcompare as cc
import os
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from plyfile import PlyData, PlyElement


##commande=LT.cloudcompare.open_file(LT.cloudcompare.open_file(LT.cloudcompare.open_file(commande0,shift,workspace+dossier+file1),
##                                                                     shift,workspace+dossier+file2),shift,workspace+dossier+corepts)
##        LT.cloudcompare.m3c2(commande,workspace+params_file)
##        new_file1=LT.cloudcompare.last_file(workspace+dossier+corepts[0:-4]+"_20*.laz",file_result)
##        new_file=LT.cloudcompare.last_file(workspace+dossier+file1[0:-4]+"_20*.laz")
##        os.remove(new_file)
##        new_file=LT.cloudcompare.last_file(workspace+dossier+file2[0:-4]+"_20*.laz")
##        os.remove(new_file)
##      

filepath = 'D:/papier_M2/Analyses/'
shift = 'New_Zealand'
filename1 = 'M3C2_3D_brut_sans_RMS.ply' 
filename2 = 'LoD_analysis/0.1.ply'
corepoints = 'core_points_2017.ply'
params_file = 'm3c2_3D_params.txt'

commande0 = 'CloudCompare -C_EXPORT_FMT PLY -AUTO_SAVE off'
commande=cc.open_file(commande0,shift,filepath+filename1)


# Extraction
extraction_range = [0.1, 0.2]# 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1]
for i in extraction_range:
    cc.seuillage(commande,6,-i,i)
   # cc.stats_test(commande,'Gauss')

# LoD_analysis

mean = [0.005, 0.008, 0.007, 0.005, 0.002, 0.001, 0.001, 0.001, 0.001, 0.001]
std  = [0.054, 0.095, 0.126, 0.150, 0.167, 0.177, 0.183, 0.187, 0.188, 0.189]

# create a group of time series
num_samples = 10
group_size = 0.1
x = np.linspace(0.1, 1, num_samples)
df = pd.DataFrame(x.T, index=range(0,num_samples))

# Add std deviation bars to the previous plot
plt.errorbar(x, mean, yerr=std, fmt='-o', capsize=5) #fmt=None to plot bars only
plt.xlabel('M3C2 threshold (m)',fontsize = 1, fontweight = 'bold')
plt.ylabel('M3C2 mean (m)',fontsize = 14, fontweight = 'bold')
plt.show()

# read ply file

filepath = 'D:/papier_M2/Analyses/'
num_samples = 10
x = np.around(np.linspace(0.1, 1, num_samples),1)
mean_M3C2 = {}
mean_LoD  = {}
std_M3C2  = {}
std_LoD   = {}

mean_M3C2_np = []
mean_LoD_np  = []
std_M3C2_np  = []
std_LoD_np   = []
for ii in x:
    name = str(ii) + '.ply'
    file_name= 'LoD_analysis/' + name
    plydata = PlyData.read(filepath+file_name)
    M3C2_distance = plydata['vertex']['scalar_M3C2_distance']
    LoD = plydata['vertex']['scalar_distance_uncertainty_reg']
    mean_M3C2['Mean{0}'.format(ii)] = np.mean(M3C2_distance)
    mean_LoD['Mean{0}'.format(ii)] = np.mean(LoD)
    std_M3C2['STD{0}'.format(ii)] = np.std(M3C2_distance)
    std_LoD['STD{0}'.format(ii)] = np.std(LoD)

ax = plt.figure(figsize=(12,5))
ax1 = ax.add_subplot(121)
for iii in x:
    mean_M3C2_np = np.append(mean_M3C2_np,mean_M3C2['Mean{0}'.format(iii)])
    std_M3C2_np  = np.append(std_M3C2_np,std_M3C2['STD{0}'.format(iii)])
    
ax1.errorbar(x, mean_M3C2_np, yerr=std_M3C2_np, fmt='-o', capsize=5)
ax1.set_xlabel('M3C2 threshold (m)',fontsize = 14, fontweight = 'bold')
ax1.set_ylabel('M3C2 mean (m)',fontsize = 14, fontweight = 'bold')


ax2 = ax.add_subplot(122)
for iv in x:
    mean_LoD_np = np.append(mean_LoD_np, mean_LoD['Mean{0}'.format(iv)])
    std_LoD_np  = np.append(std_LoD_np,std_LoD['STD{0}'.format(iv)])
ax2.errorbar(x, mean_LoD_np, yerr=std_LoD_np, fmt='-o', capsize=5)
ax2.set_xlabel('M3C2 threshold (m)',fontsize = 14, fontweight = 'bold')
ax2.set_ylabel('Mean LoD with reg (m)',fontsize = 14, fontweight = 'bold')    

left  = 0.125  # the left side of the subplots of the figure
right = 0.9   # the right side of the subplots of the figure
bottom = 0.1   # the bottom of the subplots of the figure
top = 0.9      # the top of the subplots of the figure
wspace = 0.3   # the amount of width reserved for blank space between subplots
hspace = 0.2   # the amount of height reserved for white space between subplots
plt.subplots_adjust(left, bottom, right, top, wspace, hspace)
plt.show()