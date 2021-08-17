# -*- coding: utf-8 -*-
# Thomas Bernard - 29/04/2019
import numpy as np
from scipy.stats import binned_statistic


import scripts.fit_functions as fit
import pandas as pd


def extract_arguments(list_of_arguments):
    arguments = [int(list_of_arguments[i]) for i in range(0,len(list_of_arguments))]
    return arguments
def extract_arguments_float(list_of_arguments):
    arguments = [float(list_of_arguments[i]) for i in range(0,len(list_of_arguments))]
    return arguments

def get_list_of_list(list_of_thresholds):
    """
    This function take the list of the argument thresholds, extract the value and create a list of list
    """
    extract_thresholds = [float(list_of_thresholds[i]) for i in range(0,len(list_of_thresholds))]
    n = 2        
    def chunks(l, n):
    # For item i in a range that is a length of l,
        for ii in range(0, len(l), n):
        # Create an index range for l of n items:
            yield l[ii:ii+n]
    
    thresholds = list(chunks(extract_thresholds,n))
    
    return thresholds


def del_nan_value(np_array1,np_array2,value):
    """
    First reshape two numpy arrays then delete  value like -9999 considered as nan value from a npa to another.
    """
    
    parameterX = np.reshape(np_array1,(np.size(np_array1),1))  # X array
    np.place(parameterX, parameterX == value, np.nan)          # place the value specify into nan value
    parameter1_nan_np = np.isnan(parameterX)                   # return True for each nan value and False for other values
    parameter1_np =  parameterX[np.logical_not(parameter1_nan_np)]
    
    parameterY = np.reshape(np_array2,(np.size(np_array2),1))
    parameter2_nan_np = np.isnan(parameterX)                  # return True for each nan value and False for other values
    parameter2_np = parameterY[np.logical_not(parameter2_nan_np)]
    
    return parameter1_np, parameter2_np

def slope_filter(np_array1, np_array2, min_value, max_value):
    """
    Same function than del_nan_value but take 2 value filter instead of one.
    If slope is on Y-axis
    Then slope_filter(Y,X,min_value,max_value)
    """
    
    np.place(np_array1, np.logical_or(np_array1 >= max_value, np_array1 <= min_value),np.nan)
    np_array1_nan = np.isnan(np_array1)
    np_array1_filtre = np_array1[np.logical_not(np_array1_nan)]
    
    np_array2_filtre = np_array2[np.logical_not(np_array1_nan)]

    return np_array1_filtre, np_array2_filtre

def data_filter_between(np_arrayX, np_arrayY, threshold):
    """
    This function filter data above a certain threshold value
    threshold is a list[min_value,max_value]
    """
    df_dico={'paramX_bin': np_arrayX, 'paramY_bin': np_arrayY}
    df = pd.DataFrame(df_dico,index = np.linspace(0,len(df_dico['paramX_bin']),len(df_dico['paramX_bin'])))
    
    data_filter = df[np.logical_and(df['paramX_bin'] >= threshold[0],df['paramX_bin'] <= threshold[1])] # Filter X data
 
    X_np = data_filter['paramX_bin'].to_numpy()
    Y_np = data_filter['paramY_bin'].to_numpy()

    return X_np, Y_np

    
def bin_data_center(np_array, nb_bins, bin_data,range_bin):   
    #generate logarithm bins
    np_array_bin = np.float32(np.logspace(np.log10(range_bin[0]), np.log10(range_bin[1]), num=nb_bins))
    #np_array_bin = np.float32(np.logspace(np.log10(np.min(np_array)), np.log10(np.max(np_array)), num=nb_bins))
    bin_count, _ ,bin_count_index = binned_statistic(np_array, np_array, statistic='count', bins=np_array_bin)
    bin_center, bin_edges, binnumber = binned_statistic(np_array, np_array, statistic=bin_data, bins=np_array_bin)
    
    return bin_center, bin_edges, binnumber, bin_count

def bin_data_average(np_array_x,np_array_y, nb_bins,bin_data,range_bin):
    np_array_bin = np.float32(np.logspace(np.log10(range_bin[0]), np.log10(range_bin[1]), num=nb_bins))
    #np_array_bin = np.float32(np.logspace(np.log10(np.min(np_array_x)), np.log10(np.max(np_array_x)), num=nb_bins)) 
    bin_count, _ ,bin_count_index = binned_statistic(np_array_x, np_array_y, statistic='count', bins=np_array_bin)
    bin_average, bin_edges, binnumber = binned_statistic(np_array_x, np_array_y, statistic=bin_data, bins=np_array_bin)

    
    return bin_average, bin_edges, binnumber, bin_count


    
def intercepts(paramX,paramY,dictionnary,nbfit):
    """ 
    This function create a tab of N numpy arrays and then find the X,Y value of the intercepts of the different fits
    """
    intercepts   = {}
    X_intercepts = []
    Y_intercepts = []
    
    dictionnary = list(dictionnary.values())      # extract all values of the dictionnary
    paramX = paramX.values
    paramY = paramY.values
    tab = np.reshape(paramX,(np.size(paramX),1))
    tab = np.append(tab,np.reshape(paramY,(np.size(paramY),1)),axis=1)
    for i in range(0,nbfit):
         tab = np.append(tab,np.reshape(dictionnary[i].values,(np.size(dictionnary[i].values),1)),axis=1)  # put all numpy arrays together in tab format
    for ii in range(2,1+nbfit):
        diff = np.abs(tab[:,ii+1] - tab[:,ii])
        diff = np.reshape(diff,(np.size(diff),1))
        tab  = np.append(tab,diff,axis=1)
        intercepts['I1{0}'.format(ii)] = (tab[:,0][np.min(np.where(tab[:,ii+nbfit] == np.min(tab[:,ii+nbfit])))]),tab[:,ii][np.min(np.where(tab[:,ii+nbfit] == np.min(tab[:,ii+nbfit])))]
        X_intercepts = np.append(X_intercepts,intercepts['I1{0}'.format(ii)][0])
        Y_intercepts = np.append(Y_intercepts,intercepts['I1{0}'.format(ii)][1])
        
    return X_intercepts, Y_intercepts

def slice_with_thresholds(grd,thresholds):
    
    grd[np.logical_and(grd >= thresholds[-1], grd<1e9)] = 1e9
    
    for i in range(1,len(thresholds)):
        grd[np.logical_and(np.logical_and(grd>=thresholds[i-1], grd< thresholds[i]),grd != 12*10**i-1)] = 12*10**i
    
    grd[np.logical_and(np.logical_and(grd>-9999,grd < thresholds[0]),np.logical_and(grd != 120,grd!=1e6))] = 1
    
    return grd

def deviation_map(grd_X, grd_Y, cs, a, b, X_intercept,precipitation,norm,devmap):
    """
    This function create a tab with X, Y, Ymodel values and then define positif value from X data to which the Y values are higher than the model values
    and negative values for which the Y values are lower than model values.
    """
    grd_model = np.copy(grd_X)   
    grd_model = np.where(grd_model>-9999, 10**a*grd_model**b, grd_model)
    
    grdY_Ymodel = np.where(np.logical_and(grd_Y>-9999,grd_model>-9999),grd_Y/grd_model,grd_Y)   # Divide Y values by Y model values
    
    return grdY_Ymodel
  

    
def subsample_data(np_array,nb):
    np.random.seed(3)
    sub_data = np.random.choice(np_array,int(nb))
    return sub_data



def normalize_by_rainfall(np_array,precipitation):
    precipitation = (precipitation*1e-3)/3600
    np_array = np_array/ precipitation
    
    return np_array

def normalise_by_logbin(np_array_x,np_array_y, nb_bins=60):
    value = {}
    np_array_bin = np.float32(np.logspace(np.log10(np.min(np_array_x)), np.log10(np.max(np_array_x)), num=nb_bins)) 
    bin_average, _, binnumbers= binned_statistic(np_array_x, np_array_y, statistic='mean', bins=np_array_bin)
    
    bin_average = np.nan_to_num(bin_average)

    for i in range(1,len(bin_average)+1):
        value['value{0}'.format(i)] = bin_average[i-1]
      
        binnumber_bool = binnumbers==i
        if i == 1:
            y_average_bin = binnumber_bool*value['value{0}'.format(i)]
        else:
            y_average_bin = y_average_bin + binnumber_bool*value['value{0}'.format(i)]
        
    data = np_array_y/y_average_bin
    data = np.nan_to_num(data)
    data[data>1e300] = -9999

    return data

def normalisegrid_by_logbin(grd_Y,grd_X,sizeX,sizeY):
    value = {}  
    
    grdX_bool = grd_X>-9999
    
    grdY_reshape = np.reshape(grd_Y,(np.size(grd_Y),))
    grdX_reshape = np.reshape(grd_X,(np.size(grd_X),))

    
    np_array_bin = np.float32(np.logspace(np.log10(np.min(grd_X[grdX_bool])), np.log10(np.max(grd_X[grdX_bool])), num=60))
    bin_average, _, binnumbers= binned_statistic(grdX_reshape, grdY_reshape, statistic='mean', bins=np_array_bin)
    bin_average = np.nan_to_num(bin_average)
    
    for i in range(1,len(bin_average)+1):
        value['value{0}'.format(i)] = bin_average[i-1]
        binnumber_bool = binnumbers==i
        if i == 1:
            y_average_bin = binnumber_bool*value['value{0}'.format(i)]
        else:
            y_average_bin = y_average_bin + binnumber_bool*value['value{0}'.format(i)]

    data = grdY_reshape/y_average_bin
    data = np.nan_to_num(data)
    data[np.logical_or(data<-1e300,data>1e300)] = -9999
    grid_data = np.reshape(data,(sizeY,sizeX), order=('C'))
    
    return data, grid_data

def rA_divided_by_q(bassin_versant,parameterX,parameterY,precipitation,resolution):
    water = parameterX
    q = parameterY
    # precipitation in m/s
    precipitation_ms = int(precipitation)*1e-3/3600
    
    # Get the area data
    path, filename = eros.get_path(bassin_versant, precipitation, 'vegetation', resolution)
    path_to_file = path + filename
    Area = eros.open_file(path_to_file)
    Area_grd = Area[0]
    
    width = (precipitation_ms*Area_grd)/q
    width[width<1e-7] = -9999   
      
    return width, water
    

def rA_divided_by_qh(bassin_versant,parameterX,parameterY,precipitation,resolution):
    h = parameterY
    q = parameterX
    # precipitation in m/s
    precipitation_ms = int(precipitation)*1e-3/3600
    
    # Get the area data
    path, filename = eros.get_path(bassin_versant, precipitation, 'vegetation', resolution)
    path_to_file = path + filename
    Area = eros.open_file(path_to_file)
    Area_grd = Area[0]
    
    width = (precipitation_ms*Area_grd)/(q*h)
      
    return width, q
    
        
def S_Q_derivative(paramX,paramY):
    derivative = np.diff(np.log10(paramY))/np.diff(np.log10(paramX))
    return derivative

def river_width(paramX, paramY):
    model = paramY/paramX
    
    np.nan_to_num(model,copy=False)
    model[model==0]=-9999

    d= {'paramX':paramX,'paramY':paramY,'model':model}
    df = pd.DataFrame(data=d)
    df_sup1 = df.loc[df['model'] >= 1]
    #df_around1 = df.loc[(df['model']<1) & (df['model']>=1e-2)]
    df_inf1 = df.loc[df['model'] < 1]
    paramX_sup= df_sup1['paramX'].to_numpy()
    paramY_sup = df_sup1['paramY'].to_numpy()
    model_sup = df_sup1['model'].to_numpy()
    
    #paramX_around1 = df_around1['paramX'].to_numpy()
   # paramY_around1 = df_around1['paramY'].to_numpy()
    
    paramX_inf= df_inf1['paramX'].to_numpy()
    paramY_inf = df_inf1['paramY'].to_numpy()
    modelinf=df_inf1['model'].to_numpy()
    
    return model_sup, paramX_sup, paramY_sup, paramX_inf, paramY_inf# paramX_around1, paramY_around1,
    
