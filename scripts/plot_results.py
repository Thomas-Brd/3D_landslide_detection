# -*- coding: utf-8 -*-
"""
Created on Sat May 12 14:59:09 2020

@author: tbernard
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
fontname = 'Arial'
plt.rcParams['font.style'] = 'normal'
def distribution(X,Y,n,bins,y_est,Xlabel,Ylabel,output_file,ymin,ymax,xmin,xmax,plot_fit,LoD,area,save):
    
    ax2= plt.figure(figsize=(11,9))
    plt.tick_params(axis='both',which='major',length=8,width=2)
    plt.tick_params(axis='both',which='minor',length=4,width=2)
    
    plt.plot(bins[:-1],n,'wo', markersize = 16, mec = 'k')
    if area==1:
         # Distribution landslide area Massey et al. 2020
        filepath = 'G:/papier_M2/Bibliographie/Data_Massey_2020/'
        filename = 'distribution_landslide.csv'
        column_names = ['A (m²)', 'Density (m$^-2$)']
        df = pd.read_csv(filepath+filename,sep=';',names=column_names)
        plt.plot(df['A (m²)'],df['Density (m$^-2$)'],'o',markersize = 16,mfc='gray', mec = 'k')
    if plot_fit == 1:
        plt.plot(X,y_est,'r-',zorder=3,linewidth=2)
    if LoD == 1:
        x_LoD = np.linspace(6.8,6.8,20)
        y_LoD = np.linspace(np.min(n)-0.1,np.max(n)+1,20)
        plt.plot(x_LoD, y_LoD, 'k--')
        plt.text(8,1.2e-6,"3D minimum volume",{'color':'k','fontsize':18},rotation=90)
    plt.ylim(ymin,ymax)
    plt.xlim(xmin,xmax)
    plt.xscale('log')
    plt.yscale('log')
    #plt.xlabel(Xlabel,fontsize=34,fontweight='bold',fontname=fontname)
    #plt.ylabel(Ylabel,fontsize=34,fontweight='bold',fontname=fontname)
    plt.xticks(fontsize=32)
    plt.yticks(fontsize=32)
    if save == 1:
        ax2.savefig(output_file,dpi=300)
        
        
def V_A_scaling(X,Y,c,std,area,volume,volume_err,output_file,save):
    ax= plt.figure(figsize=(10,8))
    #plt.plot(area,volume, 'ko', markersize= 2)
    y_est=10**c[0]*X**c[1]
    y_up = 10**(c[0]+std[0])*X**(c[1]+std[1])
    y_down = 10**(c[0]-std[0])*X**(c[1]-std[1])
    #plt.plot(X,Y,'ko',mfc="w", markersize=9, label='binned data',zorder=2)
    plt.plot(X,y_est,'r-',zorder=3,linewidth=3)
    plt.errorbar(area, volume, yerr=volume_err, fmt='ko',markersize=3, mfc='k',elinewidth=1, ecolor='gray', capsize=3,zorder=1, alpha=0.4)

    #plt.plot(area,y_up,'r--')
    #plt.plot(area,y_down,'r--')

    # Larsen et al. 2010
    Volume_soil = 10**(-0.37)*X**1.13
    Volume_mixed = 10**(-0.86)*X**1.36
    Volume_bedrock = 0.025*X**1.49
    plt.plot(X,Volume_soil, 'steelblue', linestyle ='dotted', linewidth=2)
    plt.plot(X,Volume_mixed, 'steelblue', linestyle = '-', linewidth=2)
    # Massey et al. 2020
    volume_all_massey = 10**(-0.05)*X**1.109
    volume_soil_massey = 10**(0.12)*X**1.06
    plt.plot(X,volume_all_massey, 'limegreen', linestyle = '-', linewidth=2)
    plt.plot(X,volume_soil_massey, 'limegreen', linestyle = 'dotted', linewidth=2)
    
    y_LoD = np.linspace(6.8,6.8,20)
    x_LoD = np.linspace(1,1e6,20)
    plt.plot(x_LoD, y_LoD, 'k--')
    plt.text(5e3,8,"3D minimum volume",{'color':'k','fontsize':15},rotation=0)
    #plt.plot(X,Volume_bedrock, 'k--')
    #plt.plot(area,volume_pred,'r-')
    # text
    plt.rc('mathtext',fontset='cm')
    y_position = 10**4
    x_position = 5*10**1
    #text = 'V = ' + str(np.round(MLE[0],2)) + 'A$^{'+ str(np.round(MLE[1],2))+'}$'
    #plt.text(x_position,y_position,text,color='r',fontsize= 22)

    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(1e-1,1e7)
    plt.xlim(8e0,1e5)
   # plt.xlabel('Area ($m^2$)',fontsize=24,fontweight='bold',fontname=fontname)
    #plt.ylabel('Volume (m$^3$)',fontsize=24,fontweight='bold',fontname=fontname)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tick_params(axis='both',which='major',length=8,width=2)
    plt.tick_params(axis='both',which='minor',length=4,width=2)
    # estimate r² for larsen
    from sklearn.metrics import r2_score
    print('R²_Vsoil = ', r2_score(Y,Volume_soil))
    print('R²_Vmixed = ', r2_score(Y,Volume_mixed))
    print('R²_Vmassey = ', r2_score(Y,volume_all_massey))
    print('R²_Vsoil_massey = ', r2_score(Y,volume_soil_massey))
    
    if save == 1:
        ax.savefig(output_file,dpi=300)
        
        
def V_A_scaling_massey(X,Y,c,std,area,volume,volume_err,output_file,save):
    ax= plt.figure(figsize=(10,8))
    #plt.plot(area,volume, 'ko', markersize= 2)
    y_est=10**c[0]*X**c[1]
    y_up = 10**(c[0]+std[0])*area**(c[1]+std[1])
    y_down = 10**(c[0]-std[0])*area**(c[1]-std[1])
    plt.plot(X,Y,'ko',mfc="w", markersize=9, label='binned data',zorder=2)
    plt.plot(X,y_est,'r-',zorder=3,linewidth=3)
    plt.errorbar(area, volume, yerr=volume_err, fmt='ko',markersize=3, mfc='k',elinewidth=1, ecolor='gray', capsize=3,zorder=1, alpha=0.4)

    #plt.plot(area,y_up,'r--')
    #plt.plot(area,y_down,'r--')

    # Larsen et al. 2010
    #Volume_soil = 0.426*X**1.13
    #Volume_mixed = 0.138*X**1.36
    #Volume_bedrock = 0.025*X**1.49
    #plt.plot(X,Volume_soil, 'steelblue', linestyle ='--', linewidth=2)
    #plt.plot(X,Volume_mixed, 'steelblue', linestyle = '-', linewidth=2)
    # Massey et al. 2020
    volume_all_massey_corrected_cleaned = 10**(-0.05)*X**1.109
    volume_soil_massey_corrected_cleaned = 10**(0.12)*X**1.06
    volume_all_massey_no_weighting = 10**(-0.23)*X**1.08
    volume_all_massey_weighted = 10**(0.34)*X**1.016
    volume_soil_massey_no_weighting = 10**(0.15)*X**0.914
    plt.plot(X,volume_all_massey_corrected_cleaned, 'limegreen', linestyle = '-', linewidth=2)
    plt.plot(X,volume_soil_massey_corrected_cleaned, 'b', linestyle = '-', linewidth=2)
    plt.plot(X,volume_all_massey_no_weighting, 'limegreen', linestyle = '--', linewidth=2)
    plt.plot(X,volume_soil_massey_no_weighting, 'b', linestyle = '--', linewidth=2)
    plt.plot(X,volume_all_massey_weighted, 'limegreen', linestyle = '-.', linewidth=2)
    
    
    
    #plt.plot(X,Volume_bedrock, 'k--')
    #plt.plot(area,volume_pred,'r-')
    # text
    plt.rc('mathtext',fontset='cm')
    y_position = 10**4
    x_position = 5*10**1
    #text = 'V = ' + str(np.round(MLE[0],2)) + 'A$^{'+ str(np.round(MLE[1],2))+'}$'
    #plt.text(x_position,y_position,text,color='r',fontsize= 22)

    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(1e-1,1e7)
    plt.xlim(8e0,1e5)
   # plt.xlabel('Area ($m^2$)',fontsize=24,fontweight='bold',fontname=fontname)
    #plt.ylabel('Volume (m$^3$)',fontsize=24,fontweight='bold',fontname=fontname)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tick_params(axis='both',which='major',length=8,width=2)
    plt.tick_params(axis='both',which='minor',length=4,width=2)
    # estimate r² for larsen
    from sklearn.metrics import r2_score
    print('R²_Vall_corrected_cleaned = ', r2_score(np.log10(Y),np.log10( volume_all_massey_corrected_cleaned)))
    print('R²_Vall_no_weighting = ', r2_score(np.log10(Y),np.log10(volume_all_massey_no_weighting)))
    print('R²_Vall_weighted = ', r2_score(np.log10(Y),np.log10(volume_all_massey_weighted )))
    print('R²_Vsoil_corrected_cleaned = ', r2_score(np.log10(Y),np.log10(volume_soil_massey_corrected_cleaned )))
    print('R²_Vsoil_no_weighting = ', r2_score(np.log10(Y),np.log10(volume_soil_massey_no_weighting)))
    
    if save == 1:
        ax.savefig(output_file,dpi=300)