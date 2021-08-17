# coding: utf-8
# Thomas Bernard
# Segmentation de Bassin versant avec TauDEM et création de fichier rain

from subprocess import Popen,PIPE,STDOUT
import subprocess
import os
import rasterio 
from rasterio.plot import show
from matplotlib import pyplot

def __test_func(value,message):
    try:
        assert(value==False)
    except:
        raise OSError(message)
        
        
def remove_pits(path,filename,plot_option):
    """
    Commande pour gérer les dépressions
    """
    commande = 'mpiexec -n 8 PitRemove -z ' + filename + '.tif -fel ' + filename + '_fill.tif'
    
    process=Popen(commande,stdout=PIPE,stderr=STDOUT)
    while process.poll() is None:
        if len(process.stdout.readline())>0:
            print(str(process.stdout.readline(),encoding='utf-8'),end="\r")
    print(str(process.stdout.read(),encoding='utf-8'))
    
    if plot_option == 1:
        src = rasterio.open(path+filename+'_fill.tif')
        show(src)
        
def flowdir(path,filename, dem_fill, plot_option,method):
    if method == 'D8':
        print('Compute flow direction (D8) : ')
        commande = 'mpiexec -n 8 D8Flowdir -p ' + filename +'p.tif -sd8 ' + filename + '_D8_flowdir.tif' +' -fel ' + dem_fill 
    else:
        print('Compute flow direction (Dinf) : ')
        commande = 'mpiexec -n 8 DinfFlowDir -fel ' + dem_fill+' -ang ' + filename + '_ang.tif' +' -slp ' + filename + '_slp.tif'
    
    process=Popen(commande,stdout=PIPE,stderr=STDOUT)
    while process.poll() is None:
        if len(process.stdout.readline())>0:
            print(str(process.stdout.readline(),encoding='utf-8'),end="\r")
    print(str(process.stdout.read(),encoding='utf-8'))
    
    if plot_option == 1:
        src = rasterio.open(path+filename + '_D8_flowdir.tif')
        show(src)
    del commande
    
def contributing_area(filename,method):
    if method == 'D8':
        print('Compute Contributing area (D8) : ')
        commande = 'mpiexec -n 8 AreaD8 -p ' + filename+ 'p.tif -ad8 ' + filename + '_D8_area.tif' +' -nc'
    else:
        print('Compute Contributing area (Dinf) : ')
        commande = 'mpiexec -n 8 AreaDinf -ang ' + filename+ '_ang.tif -sca ' + filename + '_Dinf_area.tif' +' -nc'
        
    process=Popen(commande,stdout=PIPE,stderr=STDOUT)
    while process.poll() is None:
        if len(process.stdout.readline())>0:
            print(str(process.stdout.readline(),encoding='utf-8'),end="\r")
    print(str(process.stdout.read(),encoding='utf-8'))

def upstream_distance(filename):
    commande = 'mpiexec -n 8 DinfDistUp -ang ' + filename+ '_ang.tif -fel ' + filename + '_fill.tif' +' -slp ' +filename +'_slp.tif' + ' -du '+filename+'_distanceUp.tif' + ' -m ave p' +' -thresh 0.5 ' + '-nc'
    process=Popen(commande,stdout=PIPE,stderr=STDOUT)
    while process.poll() is None:
        if len(process.stdout.readline())>0:
            print(str(process.stdout.readline(),encoding='utf-8'),end="\r")
    print(str(process.stdout.read(),encoding='utf-8'))
    
def downstream_distance(filename):
    commande = 'mpiexec -n 8 DinfDistDown -ang ' + filename+ '_ang.tif -fel ' + filename + '_fill.tif' +' -src ' +filename +'_src.tif' + ' -dd '+filename+'_distancedown.tif' + ' -m p max' + '-nc'
    process=Popen(commande,stdout=PIPE,stderr=STDOUT)
    while process.poll() is None:
        if len(process.stdout.readline())>0:
            print(str(process.stdout.readline(),encoding='utf-8'),end="\r")
    print(str(process.stdout.read(),encoding='utf-8'))
    
def grid_network(filename):
    print('Compute grid network : ')
    commande = 'mpiexec -n 8 Gridnet -p ' + filename + 'p.tif -gord '+ filename+'_gord.tif'+' -plen '+ filename+ 'plen.tif -tlen '+filename +'tlen.tif'
    
    process=Popen(commande,stdout=PIPE,stderr=STDOUT)
    while process.poll() is None:
        if len(process.stdout.readline())>0:
            print(str(process.stdout.readline(),encoding='utf-8'),end="\r")
    print(str(process.stdout.read(),encoding='utf-8'))
    
def threshold(filename, threshold):
    commande = "mpiexec -n 8 Threshold -ssa "+ filename +"_D8_area.tif -src " +filename +"_src.tif -thresh "+ threshold
    
    process=Popen(commande,stdout=PIPE,stderr=STDOUT)
    while process.poll() is None:
        if len(process.stdout.readline())>0:
            print(str(process.stdout.readline(),encoding='utf-8'),end="\r")
    print(str(process.stdout.read(),encoding='utf-8'))
    
def move_outlet(filename, shapefile):
    commande = "mpiexec -n 8 moveoutletstostreams -p " + filename + 'p.tif -src ' + filename+ '_src.tif -o '+ shapefile +' -om ' + filename+"_outlet.shp"
    
    process=Popen(commande,stdout=PIPE,stderr=STDOUT)
    while process.poll() is None:
        if len(process.stdout.readline())>0:
            print(str(process.stdout.readline(),encoding='utf-8'),end="\r")
    print(str(process.stdout.read(),encoding='utf-8'))
    
def PD_stream(filename):
    commande = "mpiexec -n 8 PeukerDouglas -fel " + filename+ '_fill.tif -ss '+ filename+"_PD_stream.tif"
    
    process=Popen(commande,stdout=PIPE,stderr=STDOUT)
    while process.poll() is None:
        if len(process.stdout.readline())>0:
            print(str(process.stdout.readline(),encoding='utf-8'),end="\r")
    print(str(process.stdout.read(),encoding='utf-8'))
    
def stream_watershed(filename, plot_option):
    commande = "mpiexec -n 8 Streamnet -fel "+ filename + "_fill.tif -p " + filename + "p.tif -ad8 "+filename+"_D8_area.tif -src "+ filename + "_src.tif -o "+filename+"_outlet.shp -ord "+ filename + "_ord.tif -tree "+ filename+"_tree.txt -coord "+filename+"_coord.txt -net "+ filename+ "net.shp -w " + filename+"_watersheds.tif"
    
    process=Popen(commande,stdout=PIPE,stderr=STDOUT)
    while process.poll() is None:
        if len(process.stdout.readline())>0:
            print(str(process.stdout.readline(),encoding='utf-8'),end="\r")
    print(str(process.stdout.read(),encoding='utf-8'))
    
    if plot_option == 1:
        src = rasterio.open(filename + '_watersheds.tif')
        show(src)
def WatershedtoShapefile(filename):
    commande = "mpiexec - n 8 WaterShedGridToShapefile"
    
    