# coding: utf-8
# Thomas Bernard
# Work environment and parameters

# Work environment
workspace = 'D:/Beyond_2D_inventories_synoptic_3D_landslide_volume_calculation_from_repeat_LiDAR_data/data_to_publish/Code/'
workflow_folder = 'Landslide_detection/'
# Data to use
Data_folder = 'data/' # folder of the LiDAR data
filenames = {'pre_EQ_lidar':'Pre_EQ_LiDAR', 'post_EQ_lidar':'Post_EQ_LiDAR', 'core_points': 'core_points'} # filenames of the LiDAR data to be compared and the core points

# Cloudcompare parameters and m3C2 parameters files
shift = "New_Zealand" # Global shift to be used by cloudcompare 
commande0 = 'CloudCompare -SILENT -C_EXPORT_FMT LAS -EXT LAZ -SEP COMMA -ADD_HEADER -AUTO_SAVE off -NO_TIMESTAMP' 
commande1 = 'CloudCompare -SILENT -C_EXPORT_FMT LAS -EXT LAZ -AUTO_SAVE off -NO_TIMESTAMP'
commande2 = 'CloudCompare -SILENT -C_EXPORT_FMT LAS -EXT LAZ -AUTO_SAVE on -NO_TIMESTAMP ' # For the segmentation step
params_folder = 'params/'
params_file_3Dm3c2 = '3D_m3c2_params' 
params_file_m3c2_nan = '3D_m3c2_params_nan'
params_file_Vm3c2 = 'Vertical_m3c2_params' # For the application of the vertical-M3C2

# Geomorphic change detection parameters
segmentation_folder = 'Source_deposit_segmentation/' # folder name where the results of the segmentation will be stored
Extraction_folder = {'sources_folder' : 'Sources/','deposits_folder' : 'Deposits/'}
Extraction_filenames = {'Erosion':'Significant_Erosion','Deposits':'Significant_Deposits'} # filenames of the significant changes
reg = 0.2 # registration error

# Segmentation by connected component parameters
individual_outputs_folder = {'Sources':'Connected_components/','Deposits':'Connected_components/'}
individual_outputs_filenames = {'Sources':'individual_sources','Deposits':'individual_deposits'}
octree_level = 11 # Define the distance between two individual cluster
min_point_per_component = 20 # Define the minimum number of points in each cluster

