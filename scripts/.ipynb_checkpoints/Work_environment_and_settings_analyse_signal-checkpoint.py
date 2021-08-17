# coding: utf-8
# Thomas Bernard
# Work environment and settings  

# Work environment
workspace = 'D:/Beyond_2D_inventories_synoptic_3D_landslide_volume_calculation_from_repeat_LiDAR_data/'
workflow_folder = 'Landslide_detection/'
# Data to use
Data_folder = 'LiDAR_Data/'
filenames = {'pre_EQ_lidar':'LiDAR_2014_clean', 'post_EQ_lidar':'LiDAR_2016_registered', 'core_points': 'core_points'} # filenames for the 3D M3C2

# Cloudcompare parameters and m3C2 parameters files
shift = 'New_Zealand'
commande0 = 'CloudCompare -SILENT -C_EXPORT_FMT LAS -AUTO_SAVE off -NO_TIMESTAMP'
params_file_3Dm3c2 = '3D_m3c2_params.txt'
params_file_m3c2_nan = '3D_m3c2_params_nan.txt'

# Geomorphic change detection parameters
segmentation_folder = 'Source_deposit_segmentation/' # folder name where the results of the segmentation will be done
Extraction_folder = {'sources_folder' : 'Sources/','deposits_folder' : 'Deposits/'}
Extraction_filenames = {'Erosion':'Significant_Erosion','Deposits':'Significant_deposits'} # filenames of the significant changes

# Vertical M3C2 parameters
params_file_Vm3c2 = 'Vertical_m3c2_params.txt'

# Segmentation by connected component parameters
individual_outputs_folder = {'Sources':'Connected_components/clouds/','Deposits':'Connected_components/clouds/'}
individual_outputs_filenames = {'Sources':'individual_sources','Deposits':'individual_deposits'}
octree_level = 11
min_point_per_component = 1


    