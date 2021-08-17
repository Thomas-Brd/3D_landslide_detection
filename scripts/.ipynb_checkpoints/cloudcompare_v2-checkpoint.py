# coding: utf-8
# Baptiste Feldmann
# Liste de fonctions utilisant CloudCompare (CC)
import subprocess
import numpy as np
from joblib import Parallel, delayed
import glob
import os

SHIFT={"Abisko":"-384000.0 -7593000.0 0.0",
       "Loire":"-436000.0 -6704000.0 0.0",
       "Semois":"-190000.0 -60000.0 0.0"}

def __test_func(value,message):
    try:
        assert(value==False)
    except:
        raise OSError(message)

def altitude_surface(workspace,file,shift):
    """
    Commande CC pour le calcul de l'alttude moyenne de la surface
    """
    file2npz(workspace,file,shift)
    tmp=np.load(workspace+file[0:-4]+".npz")
    data=tmp[tmp.files[1]]
    Z=data[:,2]
    tmp.close()
    os.remove(workspace+file[0:-4]+".npz")
    return (np.mean(Z),np.std(Z))

def c2c_dist(commande,octree_lvl=0):
    """
    Commande CC cloud2cloud distance
    """
    if octree_lvl==0:
        commande+=" -C2C_DIST -split_xyz -save_clouds"
    else:
        commande+=" -C2C_DIST -split_xyz -octree_level "+str(octree_lvl)+" -save_clouds"
        
    subprocess.call(commande)
    return True

def c2c_files(commande,workspace,motif,path_surface,shiftname,octree_lvl,nbr_job=1):
    liste_files=glob.glob(workspace+motif)
    print(str(len(liste_files))+" files found")
    liste_commandes=[]
    for f in liste_files:
        liste_commandes+=[open_file(open_file(commande,shiftname,f),shiftname,path_surface)+" -C2C_DIST -split_xyz -octree_level "+str(octree_lvl)+" -save_clouds"]

    Parallel(n_jobs=nbr_job, verbose=0)(delayed(subprocess.call)(cmd) for cmd in liste_commandes)
    liste_result=glob.glob(workspace+motif[0:-4]+"_C2C_DIST_20*.laz")
    liste_surf=glob.glob(path_surface[0:-4]+"_20*.laz")
    for f in liste_result:
        name=os.path.split(f)[-1]
        os.rename(f,workspace+name.split(sep="_C2C_DIST")[0]+"_C2C.laz")
        
    for f in liste_surf:
        os.remove(f)
    print("Process done !")


def champZ(commande):
    """
    Commande CC pour ajouter un Scalar Field pour la composante Z
    """
    commande+=" -coord_to_SF Z"
    #subprocess.call(commande)
    return commande

def create_raster(commande,grid_size,interp=False):
    """
    Commande CC pour le calcul de grille
    """
    commande+=" -rasterize -grid_step "+str(grid_size)+\
                " -vert_dir 2 -proj AVG -SF_proj AVG"
    if interp:
        commande+=" -empty_fill INTERP"

    commande+=" -output_raster_z -save_clouds"
    a=subprocess.call(commande)
    return a    

def densite(commande,radius):
    """
    Commande CC pour le calcul de densité
    """
    commande+=" -density "+str(radius)+" -type KNN -save_clouds"
    subprocess.call(commande)
    return True

def file2bin(workspace,file,shift):
    """
    Commande CC, Numpy et LasTools pour la conversion d'un fichier CC (ply, bin, txt,...)
    vers un fichier LAZ
    """
    commande0="cloudcompare -silent -no_timestamp -c_export_fmt BIN -EXT bin -auto_save OFF"
    commande1=open_file(commande0,shift,workspace+file)
    subprocess.call(commande1+" -save_clouds")
    return True

def file2laz(workspace,file,shift):
    """
    Commande CC, Numpy et LasTools pour la conversion d'un fichier CC (ply, bin, txt,...)
    vers un fichier LAZ
    """
    commande0="cloudcompare -silent -c_export_fmt LAS -EXT las -auto_save OFF"
    commande1=open_file(commande0,shift,workspace+file)
    subprocess.call(commande1+" -save_clouds")
    new_file=last_file(workspace,file[0:-5]+"*.las")
    subprocess.call("laszip -i "+new_file+" -o "+workspace+file[0:-4]+".laz")
    os.remove(new_file)
    return True

def file2npz(workspace,file,shift):
    """
    Commande CC et Numpy pour la conversion d'un fichier CC (las, laz, bin,...)
    vers un fichier NPZ compressé
    """
    commande0="cloudcompare -silent -c_export_fmt ASC -PREC 12 -SEP SEMICOLON -ADD_HEADER -EXT txt -auto_save OFF"
    commande1=open_file(commande0,shift,workspace+file)
    subprocess.call(commande1+" -save_clouds")
    filename=last_file(workspace,"*.txt")
    f=open(filename,mode='r')
    tmp=f.readline()
    tmp=tmp[2:-1]
    header=tmp.split(sep=';')
    f2=np.loadtxt(f,dtype=float,delimiter=';',skiprows=1)
    f.close()
    np.savez_compressed(workspace+file[0:-4]+".npz",header,f2)
    os.remove(filename)
    return True

def file2txt(workspace,file,shift):
    """
    Commande CC, pour la conversion d'un fichier CC (ply, bin, las,...)
    vers un fichier TXT
    """
    commande0="cloudcompare -silent -no_timestamp -c_export_fmt ASC -PREC 12 -SEP SEMICOLON -ADD_HEADER -EXT txt -auto_save OFF"
    commande1=open_file(commande0,shift,workspace+file)
    subprocess.call(commande1+" -save_clouds")
    return True


def last_file(filepath,new_name=None):
    """
    Fonction pour la recherche du dernier fichier créé selon un motif particulier
    Possibilité de le renommer
    """
    liste=glob.glob(filepath)
    time=[]
    for i in liste:
        time+=[os.path.getmtime(i)]
    file=os.path.split(liste[time.index(max(time))])
    if new_name != None :
        os.rename(file[0]+"\\"+file[1],file[0]+"\\"+new_name)
        return file[0]+"\\"+new_name
    else :
        return file[0]+"\\"+file[1]

def merge_clouds(commande):
    """
    Commande CC pour la fusion de plusieurs fichiers
    """
    commande+=" -merge_clouds -save_clouds"
    subprocess.call(commande)
    return True

def m3c2(commande,params_file):
    """
    Commande CC pour executer le plugin M3C2
    """
    commande+=" -M3C2 "+params_file+" -save_clouds"
    __test_func(subprocess.call(commande),"M3C2 failed !")
    
def open_file(commande,shiftname,filepath):
    """
    Commande CC pour l'ouverture d'un fichier
    """
    commande+=" -O -global_shift "+SHIFT[shiftname]+" "+filepath
    return commande

def ortho_wavefm(commande,filepath,param_file):
    commande+=" -fwf_o "+filepath+" -fwf_ortho "+param_file+" -fwf_save_clouds"
    a=subprocess.call(commande)
    return a

def pente(commande,indexSF):
    """
    Commande CC pour le calcul de pente (gradient de la composante Z)
    """
    commande+=" -set_active_sf "+str(indexSF)+" -SF_grad TRUE -save_clouds"
    subprocess.call(commande)
    return True

def rasterize(commande,grid_size,proj,empty):
    """
    Commande CC pour le calcul de grille
    """
    commande+=" -rasterize -grid_step "+str(grid_size)+" -vert_dir 2 -proj "\
               +proj+" -SF_proj "+proj
    if empty=="empty":
        commande+=" -output_cloud -save_clouds"
        subprocess.call(commande)
    else :
        commande+=" -empty_fill "+empty+\
                   " -output_cloud -save_clouds"
        subprocess.call(commande)
    return True

def rugosite(commande,size):
    """
    Commande CC pour le calcul de rugosité
    """
    commande+=" -rough "+str(size)+" -save_clouds"
    subprocess.call(commande)
    return True

def seuillage(commande,indexSF,mini,maxi):
    """
    Commande CC pour le seuillage d'un Scalar Field
    """
    commande+=" -set_active_sf "+str(indexSF)+" -filter_sf "\
               +str(mini)+" "+str(maxi)+" -save_clouds"
    subprocess.call(commande)
    return True

def shift_seuilAlti(file):
    """
    Fonction pour le calcul du shift à appliquer sur les coordonnées
    et du seuil sur l'alti pour éliminer les points aberrantsv
    """
    coords=lecture_coorsLAS(file)
    seuil=[np.mean(coords[2])-3*np.std(coords[2]),np.mean(coords[2])+3*np.std(coords[2])]
    shiftX=(int((5000-(coords[0]/size))/1000)-2)*1000
    shiftY=(int((5000-(coords[1]/size))/1000)-2)*1000   
    return str(shiftX)+" "+str(shiftY)+" 0.0",seuil

def subsampling(commande,min_dist):
    commande+=" -SS SPATIAL "+str(min_dist)+" -save_clouds"
    subprocess.call(commande)
    return True

def txt2npz(filepath):
    """
    Fonction pour transformer un fichier TXT en NPZ
    """
    f=open(filepath,mode='r')
    tmp=f.readline()
    tmp=tmp[2:-1]
    header=tmp.split(sep=';')
    f2=np.loadtxt(f,dtype=float,delimiter=';',skiprows=1)
    f.close()
    np.savez_compressed(filepath[0:-4]+".npz",header,f2)
    return True

    









        


