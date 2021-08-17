# coding: utf-8
# Thomas Bernard
# fonctions utilisant gdal

from osgeo import gdal
import ogr, osr
import numpy as np
#import rasterio
#from rasterio.plot import show
import subprocess
import os
import matplotlib.pyplot as plt 

#import scripts.eros_function as eros


def read_tif_file(path_to_file):
    ds = gdal.Open(path_to_file)
    gt = ds.GetGeoTransform()
    proj = ds.GetProjection()
    band= ds.GetRasterBand(1)
    mask = band.GetNoDataValue()
    array = band.ReadAsArray()
    
    return array, gt, proj, mask

def ReadRasterfile(dataset):
    """
    This function open a raster file, transform it into
    a numpy array and get information from it
    """
    
    for x in range(1, dataset.RasterCount + 1):
        band = dataset.GetRasterBand(x)
        # Projection
        projection = dataset.GetProjection()
        # Raster extent  
        upx, xres, xskew, upy, yskew, yres = dataset.GetGeoTransform()
        coordinates = [upx, xres, xskew, upy, yskew, yres]
        # Dimensions
        sizeX = dataset.RasterXSize
        sizeY = dataset.RasterYSize
        # Data as a numpy array
        array = band.ReadAsArray()
        # Get nodata value from the GDAL band object
        nodata = band.GetNoDataValue()
        #Create a masked array for making calculations without nodata values
        array = np.ma.masked_equal(array, nodata)
        type(array)
    
    
    return array, sizeX, sizeY, projection, band, coordinates
    del array, sizeX, sizeY, projection, band, coordinates

# converts coordinates to index

def bbox2ix(bbox,gt):
    xo = int(round((bbox[0] - gt[0])/gt[1]))
    yo = int(round((gt[3] - bbox[3])/gt[1]))
    xd = int(round((bbox[1] - bbox[0])/gt[1]))
    yd = int(round((bbox[3] - bbox[2])/gt[1]))
    return(xo,yo,xd,yd)

def rasclip(ras,shp):
    ds = gdal.Open(ras)
    gt = ds.GetGeoTransform()

    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(shp, 0)
    layer = dataSource.GetLayer()

    for feature in layer:

        xo,yo,xd,yd = bbox2ix(feature.GetGeometryRef().GetEnvelope(),gt)
        arr = ds.ReadAsArray(xo,yo,xd,yd)
        yield arr

    layer.ResetReading()
    ds = None
    dataSource = None
    
    return arr

def WriteGeoTIF(Tiffname, nb_xpixels, nb_ypixels, size_pixels, y_position, x_position, epsg, array):
    from osgeo import gdal, osr
    
    drv = gdal.GetDriverByName('GTiff')
    ds = drv.Create(Tiffname, nb_xpixels, nb_ypixels, 1, gdal.GDT_Float32)
    gt = [x_position, size_pixels, 0, y_position, 0,-size_pixels ]
    ds.SetGeoTransform(gt)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    ds.SetProjection(srs.ExportToWkt())
    ds.GetRasterBand(1).WriteArray(array)
    ds.GetRasterBand(1).SetNoDataValue(-9999.0)
    
    return 
 
def RastertoTXTfile(path,file, output_filename):
    ds = gdal.Open(path+file)
    translate_options = gdal.TranslateOptions(format='XYZ')
    ds = gdal.Translate(destName = path+output_filename, srcDS = ds, options = translate_options)
    return
    
def create_masks(path, filename, path_masks):
    """
    This function create a mask from a tif file
    What you need:
        A path location of the Watersheds
        A file name of the watersheds tif file
        A path to write the resulted masks
    """
    # Remove the previous folder if any
    if os.path.isdir(path_masks) == True:
        contenu=os.listdir(path_masks)
        for x in contenu:
           os.remove(path_masks+x)#on supprime tous les fichier dans le dossier
        os.rmdir(path_masks)#puis on supprime le dossier
    # Create topo folder
    dataset = gdal.Open(path +filename + '.tif', gdal.GA_ReadOnly)
    array,sizeX, sizeY, projection, band, coordinates = ReadRasterfile(dataset)
    array[array<0]=-9999
    # Get origin coordinates 
    xyzlohi = [coordinates[0],coordinates[3],coordinates[3]-sizeY,coordinates[0]+sizeX]
    # get id of watersheds
    watershed_id = np.unique(array)
    watershed_id = watershed_id[1:]
    # Create masks
    masks={}
    os.mkdir(path_masks)
    watersheds_filename = {}
    count=1
    for i in watershed_id:
        array_copy = np.copy(array)
        array_copy[array!=i] = -9999
        eros.write(array_copy,sizeX,sizeY,coordinates[1],xyzlohi,path_masks+'SBV'+str(i)+'_mask.alt')
        watersheds_filename['FN{0}'.format(count)] = 'SBV'+str(i)
        count=count+1
    
    del dataset
    return watersheds_filename

def get_outlets_coordinates(path, filename, outlet_coordinates):
    """
    This functions get the outlets coordinates for each watershed in the tif file "*_watershed.tif"
    What you need:
        A path location of the Watersheds
        A file name of the watersheds tif file
        A panda dataframe of the coordinates of all points of the river network ('*_coord.txt')
    """
    # Origine of the grid in the appropriate coordinate system
    dataset = gdal.Open(path +filename + '.tif', gdal.GA_ReadOnly)
    array, sizeX, sizeY, projection, band, coordinates = ReadRasterfile(dataset)
    outlet_coordinates['Y_origin'] = coordinates[3]
    outlet_coordinates['X_origin'] = coordinates[0]
    # Get outlet coordinates in Eros format
    outlet_coordinates['Xgrid_position'] = outlet_coordinates['X_coordinates'] - outlet_coordinates['X_origin']
    outlet_coordinates['Ygrid_position'] = outlet_coordinates['Y_origin'] - outlet_coordinates['Y_coordinates']
    outlet_coordinates['Ygrid_position']=outlet_coordinates['Ygrid_position'].astype(int)
    outlet_coordinates['Xgrid_position']=outlet_coordinates['Xgrid_position'].astype(int)
    # The coordinates are sorted by descending order of the drainage area
    outlet_coordinates.sort_values(by=['Contributing area'],ascending=False)
    outlet_coordinates.reset_index(drop=True,inplace=True)
    del dataset
    return outlet_coordinates

def filename_by_Strahler_order(path, filename):
    """
    This functions return filename in function of Strahler order 
    What you need:
        A path location of the Strahler order grid and watersheds
        A file name of the watersheds tif file and Strahler order (same one)
    """
    # Import Strahler grid
    dataset = gdal.Open(path  +filename + '_ord.tif', gdal.GA_ReadOnly)
    array_Strahler, sizeX, sizeY, projection, band, coordinates = ReadRasterfile(dataset)
    # Import Watersheds grid
    watersheds = gdal.Open(path  +filename + '_watersheds.tif', gdal.GA_ReadOnly)
    array_watersheds, sizeX, sizeY, projection, band, coordinates = ReadRasterfile(watersheds)
    # Where Strahler grid is 1 get id watersheds into list 1
    first_order_array = array_watersheds[array_Strahler==1]
    # get id of watersheds
    first_order_watershed_id = np.unique(first_order_array)
    # ohterwise get id watersheds into list 2
    bigger_order_array = array_watersheds[np.logical_and(array_Strahler!=1,array_Strahler>0)]
    bigger_order_watershed_id = np.unique(bigger_order_array)
    # save filename into dictionnary 
    first_order_Watersheds = {}
    high_order_Watersheds = {}
    # Save first order watersheds
    count = 1 
    for i in first_order_watershed_id:
        first_order_Watersheds['FN{0}'.format(count)] = 'SBV' + str(i)
        count = count + 1
    # Save higher order watersheds
    count = 1
    for ii in bigger_order_watershed_id[1:]:
        high_order_Watersheds['FN{0}'.format(count)] = 'SBV' + str(ii)
        count = count+1
    
    # Save last watersheds
    last_watershed = 'SBV2'
    
    return first_order_Watersheds, high_order_Watersheds, last_watershed 

def define_inputs_and_outlets(path,filename,Input_outlet_distance,outlet_coordinates,plot_option):
    """
    This function define the inputs coordinates and the outlet coordinates located upstream and downstream 
    What you need:
        Input_outlet_distance: Distance in meter where to locate the inputs from the detected outlets
    """
    
    # Open watershed tif file for ploting option
    dataset = gdal.Open(path+filename + '_watersheds.tif', gdal.GA_ReadOnly)
    array, sizeX, sizeY, projection, band, coordinates = ReadRasterfile(dataset)
    river_network = gdal.Open(path+filename+ '_ord.tif', gdal.GA_ReadOnly)
    river_array, sizeX, sizeY, projection, band, coordinates = ReadRasterfile(river_network)
    Y_origin = coordinates[3]
    X_origin = coordinates[0]

    # Open _coord txt file
    import pandas as pd
    header = ['X_coordinates','Y_coordinates','Distance to the downstream end of a terminal link','Elevation','Contributing area']
    tab_coord=pd.read_csv(path + filename+ '_coord.txt',sep='\t',names = header,index_col=False,usecols=[1, 2, 3,4, 5],na_values='-9999')
    # Add a line at the end of the txt file for the last outlet
    tab_coord =tab_coord.append({'X_coordinates' : 9999 , 'Y_coordinates' : 9999,'Distance to the downstream end of a terminal link':tab_coord.loc[len(tab_coord)-1,'Distance to the downstream end of a terminal link']+100},ignore_index=True)
    # chercher pour chaque Xgrid_position et Ygrid_positon si valeur après est inf alors prendre coordonnées K lignes après
    outlet_watershed_dico = {}
    input_watershed_dico = {}
    input_area_dico = {}
    count = 1
    for i in outlet_coordinates['Distance to the downstream end of a terminal link']:
        index_list = tab_coord.index[np.around(tab_coord['Distance to the downstream end of a terminal link'],3)== np.around(i,3)].tolist()

        # Lists
        input_coord_list =[]
        input_area_list=[]
        
        for ii in index_list:
            # manage the last line of the text file
            if len(tab_coord) - ii > Input_outlet_distance:
                # Take coord k lines after if the +1 line is smaller  
                if np.logical_and(tab_coord.loc[ii+1,'Distance to the downstream end of a terminal link'] < tab_coord.loc[ii,'Distance to the downstream end of a terminal link'],np.abs(tab_coord['Distance to the downstream end of a terminal link'][ii+1]-tab_coord['Distance to the downstream end of a terminal link'][ii])<10)  :
                    outlet_watershed_dico['Outlet{0}'.format(count)] = [tab_coord.loc[ii+Input_outlet_distance,'X_coordinates'],tab_coord.loc[ii+Input_outlet_distance,'Y_coordinates']]
          
            # get the input coordinates
            if np.logical_or(tab_coord.loc[ii+1,'Distance to the downstream end of a terminal link'] > tab_coord.loc[ii,'Distance to the downstream end of a terminal link'],np.abs(tab_coord['Distance to the downstream end of a terminal link'][ii+1]-tab_coord['Distance to the downstream end of a terminal link'][ii])>10):
                input_coord_list.append([tab_coord.loc[ii-Input_outlet_distance,'X_coordinates'],tab_coord.loc[ii-Input_outlet_distance,'Y_coordinates']])
                input_area_list.append(tab_coord.loc[ii-Input_outlet_distance,'Contributing area'])
        input_watershed_dico['Input{0}'.format(count)] = input_coord_list
        input_area_dico['Area{0}'.format(count)] = input_area_list
        count= count + 1
      
    # transform coordinates in grid format in each dictionnary
    for j in outlet_watershed_dico:
        outlet_watershed_dico[str(j)] = [outlet_watershed_dico[str(j)][0]-X_origin, Y_origin - outlet_watershed_dico[str(j)][1]]
        outlet_watershed_dico[str(j)][0] = outlet_watershed_dico[str(j)][0].astype(int)
        outlet_watershed_dico[str(j)][1] = outlet_watershed_dico[str(j)][1].astype(int)
    
    for g in range(1,len(input_watershed_dico)+1):
        for gg in range(0,len(input_watershed_dico['Input{0}'.format(g)])):
            input_watershed_dico['Input{0}'.format(g)][gg] = [input_watershed_dico['Input{0}'.format(g)][gg][0]-X_origin, Y_origin - input_watershed_dico['Input{0}'.format(g)][gg][1]]
            input_watershed_dico['Input{0}'.format(g)][gg][0] = input_watershed_dico['Input{0}'.format(g)][gg][0].astype(int)
            input_watershed_dico['Input{0}'.format(g)][gg][1] = input_watershed_dico['Input{0}'.format(g)][gg][1].astype(int)

    
    # plot coordinates
    if plot_option == 1:
        fig, ax = plt.subplots(1, figsize=(20, 20))
        plt.imshow(array)
        masked_river = np.ma.masked_where(river_array < 1, river_array)
        plt.imshow(masked_river,cmap=plt.cm.gray)
        # plot all input and outlet points
        for y in outlet_watershed_dico:
            plt.plot(outlet_watershed_dico[str(y)][0],outlet_watershed_dico[str(y)][1],'k.',markersize=10)
        for p in range(1,len(input_watershed_dico)+1):
             for pp in range(0,len(input_watershed_dico['Input{0}'.format(p)])):
                    plt.plot(input_watershed_dico['Input{0}'.format(p)][pp][0],input_watershed_dico['Input{0}'.format(p)][pp][1],'r.',markersize=10)
    del dataset
    return outlet_watershed_dico, input_watershed_dico, input_area_dico





def sort_watersheds(path_masks,Watersheds_filename, outlet_watershed_dico,last_watershed):
    """
    This function classify the watersheds by contributing area order
    """
    list_watersheds = []
    list_position = []
    for i in range(1,len(Watersheds_filename)+1):
        grd_mask, sizeX, sizeY, cs, xyzlohi = eros.open_file(path_masks+Watersheds_filename['FN{0}'.format(i)]+'_mask.alt')
        if np.size(grd_mask) - np.size(grd_mask[grd_mask==-9999]) < 50:
            pass
        else:
            for ii in range(1,len(outlet_watershed_dico)+1):
                if grd_mask[outlet_watershed_dico['Outlet{0}'.format(ii)][1],outlet_watershed_dico['Outlet{0}'.format(ii)][0]] == np.max(grd_mask):
                    list_watersheds.append(Watersheds_filename['FN{0}'.format(i)])
                    list_position.append(ii)
                                                             
    watershed_classified = [x for _,x in sorted(zip(list_position,list_watersheds ))]

    watershed_classified_dico={}
    watershed_classified_dico['FN1'] = last_watershed
    for j in range(0,len(watershed_classified)):
        watershed_classified_dico['FN{0}'.format(j+2)] = watershed_classified[j]
        
    return watershed_classified_dico
    
    
    
def merge_results(path_topo,path_simulations,path_masks,path_tif_foleder,Watershed_name,all_watersheds_filename,extension_dico, results_folders,epsg,y_position,x_position):
    """
    This function allows to merge all the eros file results into one
    """
    array = {}
    masks ={}
    # Open array topo
    array['Ar0'], sizeX, sizeY, cs, xyzlohi = eros.open_file(path+Watershed_name+'.alt')
    for i in range(1, len(results_extension)+1):
        count=1
        for ii in results_folders:
            # Open simulation result
            array['Ar{0}'.format(count)], sizeX, sizeY, cs, xyzlohi = eros.open_file(path_simulations+ii+'/'+Watershed_name+'.10.'+results_extension['Ext{0}'.format(i)])
            # Open simulation result Open corresponding mask
            masks['masks{0}'.format(count)], sizeX, sizeY, cs, xyzlohi = eros.open_file(path_masks +all_watersheds_filename['FN{0}'.format(count)]+'_mask.alt')
            # 
            array['Ar0'][masks['masks{0}'.format(count)]>=0] = array['Ar{0}'.format(count)][masks['masks{0}'.format(count)]>=0]
            count = count + 1
        eros.write(array['Ar0'],sizeX, sizeY, cs, xyzlohi,path_floodos_folder+Watershed_name+'.10.'+results_extension['Ext{0}'.format(i)])
        gdalf.WriteGeoTIF(path_tif_folder+Watershed_name+'_'+results_extension['Ext{0}'.format(i)]+'.tif', sizeX, sizeY, cs, y_position, x_position, epsg, array['Ar1'])
