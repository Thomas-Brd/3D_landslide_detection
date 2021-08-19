# coding: utf-8
# Thomas Bernard
# Functions  
import pandas as pd
import numpy as np
import subprocess,os
import laspy
from laspy.file import File
from scripts.parameters import *
import scripts.cloudcompare as cc
import scripts.os_functions as osf
import warnings
warnings.filterwarnings("ignore")

def compute_SNR(path,filename):
    """
    This function allows to compute the signal-to-noise ratio (SNR) for a given point cloud.
    """
    # rename the input file
    os.rename(path+filename+'.laz', path+filename+'_origin'+'.laz')
    inFile = File(path+filename+'_origin.laz', mode='r')
    outFile = laspy.file.File(path+filename+'.las', mode = "w", header = inFile.header)
    
    outFile.define_new_dimension(name = "signal_to_noise_ratio",
                        data_type = 9, description = "Test Dimension")
     # Lets go ahead and copy all the existing data from inFile:
    for dimension in inFile.point_format:
        dat = inFile.reader.get_dimension(dimension.name)
        outFile.writer.set_dimension(dimension.name, dat)

    # Now lets put data in our new dimension
    # (though we could have done this first)

    # Note that the data type 5 refers to a long integer
    M3C2_distance = np.abs(inFile.points['point']['M3C2_distance_3D'])
    distance_uncertainty = inFile.points['point']['distance_uncertainty_3D'] 
    SNR = M3C2_distance/distance_uncertainty
    outFile.points['point']['signal_to_noise_ratio'] = SNR
    inFile.close()
    outFile.close()
    do_compression(path+filename+'.las')
    os.remove(path+filename+'_origin'+'.laz')
    
def compute_LoD(path,filename,reg):
    """
    This function allows to compute the M3C2 distance uncertainty (LoD95%) according to eq.(2) in (Bernard et al. 2021).
    reg : registration error
    The ouput is a point cloud with two additional scalar fields: "distance_uncertainty_3D" and "significant_change_LoD"
    """
    inFile = File(path+filename+'.laz', mode='r')
    Sd1 = inFile.points['point']['STD_cloud1']
    Sd2 = inFile.points['point']['STD_cloud2']
    Npt1 = inFile.points['point']['Npoints_cloud1']
    Npt2 = inFile.points['point']['Npoints_cloud2']
    M3C2_3D = inFile.points['point']['M3C2_distance']
    from scipy import stats
    #Compute new coefficient
    SE = np.sqrt(Sd1**2/Npt1+Sd2**2/Npt2)
    SE1 = Sd1/np.sqrt(Npt1) # Standard error of Ptcloud 1
    SE2 = Sd2/np.sqrt(Npt2) # Standard error of Ptcloud 2
    # Degree of freedom according to welch's test
    nu = SE**4/((SE1**4/(Npt1-1))+(SE2**4/(Npt2-1)))
    # Confidence interval based on the t-statistics at 95% interval for a
    # paired test (that is 0.975 for an unpaired test)
    new_LoD=stats.t.ppf(0.975,nu)*(SE+reg)
    # set nan where Npoints_cloud1 or 2 is < 4
    new_LoD[Npt1<4] = np.nan
    new_LoD[Npt2<4] = np.nan
    # New significant changes
    sig_test=np.abs(M3C2_3D)>=new_LoD
    significant = np.copy(new_LoD)
    significant[sig_test==True] = 1
    significant[sig_test==False] = 0
    inFile.close()
    #Write result in a sclar field
    SF_name1 = 'distance_uncertainty_3D'
    SF_name2 = 'significant_change_LoD'
    write_new_SF(path,filename,SF_name1,new_LoD)
    write_new_SF(path,filename,SF_name2,significant)
    
    
    
def do_compression(filename):
    """
    This function allows to compress a ".las" file to a ".laz" file.
    filename : path + filename
    """
    query="laszip -i "+filename+" -olaz"
    subprocess.run(query)
    os.remove(filename)



def extract_erosion_deposition(path,filename,segmentation_folder,Extraction_folder,Extraction_filenames):
    """
    This function allows to create 2 point clouds from one point cloud. One corresponds to the positive 
    M3C2 values (deposits) and the other to the negative M3C2 values (erosion).
    """
    inFile = File(path+filename, mode='r')
    deposits = inFile.points['point']['M3C2_distance'] > 0
    erosion = inFile.points['point']['M3C2_distance'] < 0
    outFile1 = File(path+segmentation_folder+list(Extraction_folder.values())[1]+list(Extraction_filenames.values())[1]+'.las', mode='w', header=inFile.header)
    outFile1.points = inFile.points[deposits]
    outFile1.close()
    outFile2 = File(path+segmentation_folder+list(Extraction_folder.values())[0]+list(Extraction_filenames.values())[0]+'.las', mode='w', header=inFile.header)
    outFile2.points = inFile.points[erosion]
    outFile2.close()
    inFile.close()
    do_compression(path+segmentation_folder+list(Extraction_folder.values())[0]+list(Extraction_filenames.values())[0]+'.las')
    do_compression(path+segmentation_folder+list(Extraction_folder.values())[1]+list(Extraction_filenames.values())[1]+'.las')
    
    
def extract_SC(path,filename):
    """
    This function extract all points from a point cloud that have a significant change = 1.
    """
    inFile = File(path+filename, mode='r')
    I = inFile.significant_change_LoD > 0
    outFile1 = File(path+'Significant_changes.las', mode='w', header=inFile.header)
    outFile1.points = inFile.points[I]
    outFile1.close()
    inFile.close()
    do_compression(path+'Significant_changes.las')


    
def extract_landslide_ptcloud(path,filename):
    import laspy
    from laspy.file import File
    """
    This function filter a point cloud based on the id.
    """
    osf.create_folder(path+'clouds/')
    # import id
    id_landslide = open_las(path,filename+'.laz','id')
    id_landslide_unique = np.unique(id_landslide)
    inFile = File(path+filename+'.laz',mode='r')
    for i in id_landslide_unique:
        mask = np.copy(id_landslide)
        mask[mask==i]=6000 # 1 if considered landslide
        mask = mask ==6000
        # Filter point cloud
        outFile1 = File(path+'clouds/'+filename+'_CC'+str(int(i))+'.las', mode='w', header=inFile.header)
        outFile1.points = inFile.points[mask]
        outFile1.close()
        do_compression(path+'clouds/'+filename+'_CC'+str(int(i))+'.las')
    inFile.close()


def landslide_segmentation(path_segmentation,individual_outputs_folder,individual_outputs_filenames,shift,commande1,commande2,octree_level,min_point_per_component):
    SHIFT={"New_Zealand":"-1617440.0 -5299200.0 0.0"}
    
    dir_name = path_segmentation+individual_outputs_folder + 'clouds/'
    osf.create_folder(dir_name)
    # Create individual clouds and store the result in las files
    commande = cc.open_file(commande2,shift,path_segmentation+'Vertical_M3C2.laz')
    cc.connected_component_clouds(commande,octree_level,min_point_per_component)
    # estimate the number of sources and deposits
    file_count =  len([name for name in os.listdir(path_segmentation) if os.path.isfile(os.path.join(path_segmentation, name))])
    for ii in range(1, file_count):
        os.rename(path_segmentation+'Vertical_M3C2_COMPONENT_'+str(ii)+'.laz',dir_name+'CC_'+str(ii-1)+'.laz')
        # Add a new scalar field defining the id of the point cloud
        inFile = File(dir_name+'CC_'+str(ii-1)+'.laz', mode='r')
        M3C2_3D = inFile.points['point']['M3C2_distance_3D']
        inFile.close()
        SF_array = M3C2_3D *0 + ii-1 # define the value of the scalar field id
        write_new_SF(dir_name,'CC_'+str(ii-1),'id',SF_array)
            
    clouds_name = []
    Points = []
    id_number = []
    meanX = []
    meanY = []
    meanZ = []
    mean_M3C2_vertical = []
    std_M3C2_vertical = []
    sum_M3C2_vertical = []
    mean_Duncertainty_vertical = []
    std_Duncertainty_vertical = []
    sum_Duncertainty_vertical = []
    mean_M3C2_3D = []
    std_M3C2_3D = []
    sum_M3C2_3D = []   
    mean_Duncertainty_3D = []
    std_Duncertainty_3D = []
    sum_Duncertainty_3D = []
    mean_signal_ratio_list = []
    mean_signal_ratio_list2 = []
    std_signal_ratio = []
    sum_signal_ratio = []
    mean_STD_cloud1 = []
    mean_STD_cloud2 = []
    mean_Npoints_cloud1 = []
    mean_Npoints_cloud2 = []
        
    for iii in range(0,file_count-1):
        inFile = File(dir_name+'CC_'+str(iii)+'.laz', mode='r')
        M3C2_3D = inFile.points['point']['M3C2_distance_3D']
        Duncertainty_3D = inFile.points['point']['distance_uncertainty_3D']
        signal_ratio = inFile.signal_to_noise_ratio
        mean_signal_ratio = np.mean(signal_ratio) 
                
        # Save remaining cloud names
        clouds_name = np.append(clouds_name,'CC_'+str(iii))
        id_number = np.append(id_number, np.max(inFile.points['point']['id']))
        Points = np.append(Points, len(inFile.X))
        meanX = np.append(meanX,np.mean(inFile.X))
        meanY = np.append(meanY,np.mean(inFile.Y))
        meanZ = np.append(meanZ,np.mean(inFile.Z))
        M3C2_vertical = inFile.points['point']['M3C2_distance']
        M3C2_vertical = M3C2_vertical[np.isnan(M3C2_vertical)==False]
        mean_M3C2_vertical = np.append(mean_M3C2_vertical,np.mean(M3C2_vertical))
        std_M3C2_vertical = np.append(std_M3C2_vertical, np.std(M3C2_vertical))
        sum_M3C2_vertical = np.append(sum_M3C2_vertical, np.sum(M3C2_vertical))
                
        Duncertainty_vertical= inFile.points['point']['distance_uncertainty']
        Duncertainty_vertical = Duncertainty_vertical[np.isnan(Duncertainty_vertical)==False]
        mean_Duncertainty_vertical = np.append(mean_Duncertainty_vertical,np.mean(Duncertainty_vertical))
        std_Duncertainty_vertical = np.append(std_Duncertainty_vertical, np.std(Duncertainty_vertical))
        sum_Duncertainty_vertical = np.append(sum_Duncertainty_vertical, np.sum(Duncertainty_vertical))
                
        mean_M3C2_3D = np.append(mean_M3C2_3D,np.mean(M3C2_3D))
        std_M3C2_3D = np.append(std_M3C2_3D, np.std(M3C2_3D))
        sum_M3C2_3D = np.append(sum_M3C2_3D, np.sum(M3C2_3D))
                
        mean_Duncertainty_3D = np.append(mean_Duncertainty_3D,np.mean(Duncertainty_3D))
        std_Duncertainty_3D = np.append(std_Duncertainty_3D, np.std(Duncertainty_3D))
        sum_Duncertainty_3D = np.append(sum_Duncertainty_3D, np.sum(Duncertainty_3D))

        Npoints_cloud1 = inFile.points['point']['Npoints_cloud1_3D']
        mean_Npoints_cloud1 = np.append(mean_Npoints_cloud1,np.mean(Npoints_cloud1))

        Npoints_cloud2 = inFile.points['point']['Npoints_cloud2_3D']
        mean_Npoints_cloud2 = np.append(mean_Npoints_cloud2,np.mean(Npoints_cloud2))

        STD_cloud1 = inFile.points['point']['STD_cloud1_3D']
        mean_STD_cloud1 = np.append(mean_STD_cloud1,np.mean(STD_cloud1))

        STD_cloud2 = inFile.points['point']['STD_cloud2_3D']
        mean_STD_cloud2 = np.append(mean_STD_cloud2,np.mean(STD_cloud2))

        mean_signal_ratio_list = np.append(mean_signal_ratio_list,mean_signal_ratio)
        std_signal_ratio = np.append(std_signal_ratio,np.std(signal_ratio))
        sum_signal_ratio = np.append(sum_signal_ratio,np.sum(signal_ratio))
                
        inFile.close()
            
                
    df_dico = {'Name':clouds_name, 'id': id_number, 'Points':Points, 'MeanX':meanX, 'MeanY':meanY, 'MeanZ':meanZ,
                  'Mean_M3C2_distance_3D':mean_M3C2_3D, 'Std_M3C2_distance_3D':std_M3C2_3D, 'Sum_M3C2_distance_3D':sum_M3C2_3D,
                  'Mean_3D_distance_uncertainty':mean_Duncertainty_3D, 'Std_3D_distance_uncertainty':std_Duncertainty_3D, 'Sum_3D_distance_uncertainty':sum_Duncertainty_3D,
                  'Mean_M3C2_distance_vertical':mean_M3C2_vertical, 'Std_M3C2_distance_vertical':std_M3C2_vertical, 'Sum_M3C2_distance_vertical':sum_M3C2_vertical,
                  'Mean_Duncertainty_vertical': mean_Duncertainty_vertical, 'Std_Duncertainty_vertical': mean_Duncertainty_vertical, 'Sum_Duncertainty_vertical': mean_Duncertainty_vertical, 'Mean_Npoints_cloud1_3D': mean_Npoints_cloud1, 'Mean_Npoints_cloud2_3D': mean_Npoints_cloud2, 'Mean_STD_cloud1_3D': mean_STD_cloud1, 'Mean_STD_cloud2_3D':mean_STD_cloud2,'Mean_SNR_ratio':mean_signal_ratio_list, 'Std_SNR_ratio': std_signal_ratio, 'Sum_SNR_ratio':sum_signal_ratio,}
        
    df = pd.DataFrame(data=df_dico)
        
    # Merge all files
    if len(clouds_name) > 0:
        Nb_merge = int(len(clouds_name)/2) # set the number of clouds to be merged at once maximum is 129. It has to remain under the len of clouds_name
        if Nb_merge > 129:
            Nb_merge= 129
        cloud_names_arange = np.arange(0,len(clouds_name),Nb_merge)
            
        if len(clouds_name) == 1:
            pass
        else:
            for j in cloud_names_arange:
                commande = cc.open_file(commande1,shift,dir_name+clouds_name[0]+'.laz')
            
                if j == cloud_names_arange[-1]:
                    for jj in range(0,len(clouds_name)-j):
                        commande = cc.open_file(commande,shift,dir_name+clouds_name[j+jj]+'.laz')
                    cc.merge_clouds(commande)
                    os.remove(dir_name+clouds_name[0]+'.laz')
                    for jjj in range(0,len(clouds_name)-j):
                        os.remove(dir_name+clouds_name[j+jjj]+'.laz')
                    os.rename(dir_name+clouds_name[0]+'_MERGED'+'.laz',path_segmentation+individual_outputs_folder+individual_outputs_filenames+'_merged.laz')
                else:
                    for jj in range(0,Nb_merge):
                        if j == 0:
                               commande = cc.open_file(commande,shift,dir_name+clouds_name[j+1+jj]+'.laz')
                        else:
                            commande = cc.open_file(commande,shift,dir_name+clouds_name[j+jj]+'.laz')
                        
                    cc.merge_clouds(commande)
                    for jjj in range(0,Nb_merge):
                        os.remove(dir_name+clouds_name[j+jjj]+'.laz')
                    if j > 0:
                        os.remove(dir_name+clouds_name[0]+'.laz')
                    os.rename(dir_name+clouds_name[0]+'_MERGED'+'.LAZ',dir_name+clouds_name[0]+'.laz')
    # delete clouds folder
    os.rmdir(dir_name)
    return df
   


def open_las(path,filename, scalar_field):
    inFile = File(path+filename, mode='r')

    # Note that the data type 5 refers to a long integer
    array = inFile.points['point'][scalar_field]
    
    inFile.close()
    return array
    
def read_landslide_prop(path, filenames):
    """
    This function allows to read and display some basic landslide properties.
    path: path to the landslide results
    filenames: dictionary with the sources and deposits filenames.
    """
    # Read .csv files into a dataframe
    dataframes={'Sources': pd.read_csv(path+filenames['Sources'],sep=';'),'Deposits': pd.read_csv(path+filenames['Deposits'],sep=';')}
    # Set the variables
    number_of_clouds = []
    area_range = []
    Total_area = []
    volume_range = []
    Total_volume = []
    uncertainty_volume_range = []
    Uncertainty_Total_volume = []
    # Select Area, volume and uncertainty
    for i in range(0,len(dataframes)):
        number_of_clouds.append(len(list(dataframes.values())[i]))
        area_range.append([list(dataframes.values())[i]['Points'].min(),list(dataframes.values())[i]['Points'].max()])
        Total_area.append(list(dataframes.values())[i]['Points'].sum())
        volume_range.append([np.around(list(dataframes.values())[i]['Sum_M3C2_distance_vertical'].abs().min(),2),np.around(list(dataframes.values())[i]['Sum_M3C2_distance_vertical'].abs().max(),2)])
        Total_volume.append(np.around(list(dataframes.values())[i]['Sum_M3C2_distance_vertical'].abs().sum(),0))
        uncertainty_volume_range.append([list(dataframes.values())[i]['Sum_3D_distance_uncertainty'].min(),list(dataframes.values())[i]['Sum_3D_distance_uncertainty'].max()])
        Uncertainty_Total_volume.append(np.around(list(dataframes.values())[i]['Sum_3D_distance_uncertainty'].sum(),0))
        
    # Range data into a dataframe
    df_dico={'Number of sources/deposits':number_of_clouds,'Range of area (m² ; [min,max])':area_range,'Total area (m²)':Total_area,
        'Range of volume (m$^3$)':volume_range,'Total volume (m$^3$)': Total_volume, '3D uncertainty on total volume':Uncertainty_Total_volume}
    Dataframe = pd.DataFrame(df_dico,index=['Sources','Deposits'])
    
    return Dataframe
    
    
    
def split_laz(path,filename,):
    inFile = File(path+filename, mode='r')
    I = inFile.distance_uncertainty > 0
    O = np.isnan(inFile.distance_uncertainty)
    outFile1 = File(path+'3D_M3C2_split_temp.las', mode='w', header=inFile.header)
    outFile1.points = inFile.points[I]
    outFile1.close()
    do_compression(path+'3D_M3C2_split_temp.las')
    outFile2 = File(path+'3D_M3C2_nan_temp.las', mode='w', header=inFile.header)
    outFile2.points = inFile.points[O]
    outFile2.close()
    do_compression(path+'3D_M3C2_nan_temp.las')
    inFile.close()
    
def write_new_SF(path,filename,SF_name,SF_array):
    """
    This function allows to write a new scalar field from a LAS file
    """
    import copy
    import os
    # rename the input file
    os.rename(path+filename+'.laz', path+filename+'_origin'+'.laz')
    # Set up our input and output files.
    inFile = laspy.file.File(path+filename+'_origin.laz', mode = "r")
    outFile = laspy.file.File(path+filename+'.las', mode = "w",
            header = inFile.header)
    # Define our new dimension. Note, this must be done before giving
    # the output file point records.
    outFile.define_new_dimension(name = SF_name,
                        data_type = 9, description = "Test Dimension")

    # Lets go ahead and copy all the existing data from inFile:
    for dimension in inFile.point_format:
        dat = inFile.reader.get_dimension(dimension.name)
        outFile.writer.set_dimension(dimension.name, dat)

    # Now lets put data in our new dimension
    # (though we could have done this first)

    # Note that the data type 5 refers to a long integer
    outFile.points['point'][SF_name] = SF_array
    inFile.close()
    outFile.close()
    do_compression(path+filename+'.las')
    os.remove(path+filename+'_origin'+'.laz')
    
    
def writeExtraFields(path,filename):
    import copy
    # rename the input file
    os.rename(path+filename+'.laz', path+filename+'_origin'+'.laz')
    # Set up our input and output files.
    inFile = laspy.file.File(path+filename+'_origin.laz', mode = "r")
    outFile = laspy.file.File(path+filename+'.las', mode = "w",
            header = inFile.header)
    # Define our new dimension. Note, this must be done before giving
    # the output file point records.
    outFile.define_new_dimension(name = "M3C2_distance_3D",
                        data_type = 9, description = "Test Dimension")
    outFile.define_new_dimension(name = "Npoints_cloud1_3D",
                        data_type = 9, description = "Test Dimension")
    outFile.define_new_dimension(name = "Npoints_cloud2_3D",
                        data_type = 9, description = "Test Dimension")
    outFile.define_new_dimension(name = "STD_cloud1_3D",
                        data_type = 9, description = "Test Dimension")
    outFile.define_new_dimension(name = "STD_cloud2_3D",
                        data_type = 9, description = "Test Dimension")


    # Lets go ahead and copy all the existing data from inFile:
    for dimension in inFile.point_format:
        dat = inFile.reader.get_dimension(dimension.name)
        outFile.writer.set_dimension(dimension.name, dat)

    # Now lets put data in our new dimension
    # (though we could have done this first)

    # Note that the data type 5 refers to a long integer
    new_M3C2 = copy.copy(inFile.points['point']['M3C2_distance'])
    new_Nptcloud1 = copy.copy(inFile.points['point']['Npoints_cloud1'])
    new_Nptcloud2 = copy.copy(inFile.points['point']['Npoints_cloud2'])
    new_STDcloud1 = copy.copy(inFile.points['point']['STD_cloud1'])
    new_STDcloud2 = copy.copy(inFile.points['point']['STD_cloud2'])
    outFile.points['point']['M3C2_distance_3D'] = new_M3C2
    outFile.points['point']['Npoints_cloud1_3D'] = new_Nptcloud1
    outFile.points['point']['Npoints_cloud2_3D'] = new_Nptcloud2
    outFile.points['point']['STD_cloud1_3D'] = new_STDcloud1
    outFile.points['point']['STD_cloud2_3D'] = new_STDcloud2
    inFile.close()
    outFile.close()
    do_compression(path+filename+'.las')
    os.remove(path+filename+'_origin'+'.laz')
    

    
    
