# coding: utf-8
# Thomas Bernard
# functions using CloudCompare (CC)
import subprocess
SHIFT={"New_Zealand":"-1617440.0 -5299200.0 0.0"} # Shift to apply to the data by CLoudcompare

def __test_func(value,message):
    try:
        assert(value==False)
    except:
        raise OSError(message)

def connected_component(commande,octree_level,min_point_per_component):
    commande += ' -EXTRACT_CC '+str(octree_level) + ' ' + str(min_point_per_component)+ ' -SAVE_CLOUDS ALL_AT_ONCE '
    subprocess.call(commande)
    return True

def connected_component_clouds(commande,octree_level,min_point_per_component):
    commande += ' -EXTRACT_CC '+str(octree_level) + ' ' + str(min_point_per_component)+ ' -SAVE_CLOUDS'
    subprocess.call(commande)
    return True

def merge_clouds(commande):
    """
    Commande CC pour la fusion de plusieurs fichiers
    """
    commande+=" -merge_clouds -save_clouds"
    subprocess.call(commande)
    return True

def m3c2(commande,params_folder,params_file):
    """
    Commande CC pour executer le plugin M3C2
    filenames: Names of the LiDAR point clouds used
    """
    commande+=" -M3C2 "+params_folder+params_file + " -save_clouds " 
    subprocess.call(commande)
    return True

def open_file(commande,shiftname,filepath):
    """
    Commande CC pour l'ouverture d'un fichier
    """
    commande+=" -O -global_shift "+SHIFT[shiftname]+" "+filepath 
    return commande


def close_files():
    commande = 'CloudCompare -SILENT -CLEAR -CLEAR_CLOUDS'
    subprocess.call(commande)





        


