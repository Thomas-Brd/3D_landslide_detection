# coding: utf-8
# Thomas Bernard
# Liste de fonctions utilisant CloudCompare (CC)
import subprocess
import numpy as np
from joblib import Parallel, delayed
import glob
import os

SHIFT={"New_Zealand":"-1617440.0 -5299200.0 0.0"}

def __test_func(value,message):
    try:
        assert(value==False)
    except:
        raise OSError(message)

def connected_component(commande,octree_level,min_point_per_component):
    commande += ' -EXTRACT_CC '+str(octree_level) + ' ' + str(min_point_per_component)+ ' -SAVE_CLOUDS ALL_AT_ONCE '
    subprocess.call(commande)
    return True

def filter_SF(commande,indexSF,min,max):
    """
    Commande CC pour le seuillage d'un Scalar Field
    """
    commande+=" -set_active_sf "+str(indexSF)+" -filter_sf "+str(min)+" "+str(max)+" -save_clouds " 
    subprocess.call(commande)
    return 

def merge_clouds(commande):
    """
    Commande CC pour la fusion de plusieurs fichiers
    """
    commande+=" -merge_clouds -save_clouds"
    subprocess.call(commande)
    return True

def m3c2(commande,params_file,workspace,Data_folder,filenames,file_extension):
    """
    Commande CC pour executer le plugin M3C2
    filenames: Names of the LiDAR point clouds used
    """
    commande+=" -M3C2 "+params_file + " -save_clouds " 
    subprocess.call(commande)
    # Keep only M3C2 file
    if list(filenames.values())[-1]!='core_points':
            for i in range(0,len(filenames)-1):
                os.remove(workspace+Data_folder+list(filenames.values())[i]+file_extension)
    else:
        for i in range(0,len(filenames)):
            os.remove(workspace+Data_folder+list(filenames.values())[i]+file_extension)
            
            
    
    return True

def open_file(commande,shiftname,filepath):
    """
    Commande CC pour l'ouverture d'un fichier
    """
    commande+=" -O -global_shift "+SHIFT[shiftname]+" "+filepath 
    return commande






    









        


