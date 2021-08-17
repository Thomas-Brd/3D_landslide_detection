# coding: utf-8
# Thomas Bernard

from scripts.parameters import *
import os
import importlib
import numpy as np
import pandas as pd
import scripts.cloudcompare as cc
import scripts.os_functions as osf
import scripts.functions as fc

def Geomorphic_change_detection():
    # Create the workflow folder
    osf.open_folder(workspace+workflow_folder)

    # Compute 3D-M3C2
    commande = cc.open_file(cc.open_file(cc.open_file(commande0,shift,workspace+Data_folder+filenames['pre_EQ_lidar']+'.laz'),shift,workspace+Data_folder+filenames['post_EQ_lidar']+'.laz'),shift,workspace+Data_folder+filenames['core_points']+'.laz')
    cc.m3c2(commande,workspace+params_folder,params_file_3Dm3c2 +'.txt')
    os.rename(workspace+Data_folder+list(filenames.values())[0]+'_M3C2.laz',workspace+workflow_folder+'3D_M3C2_temp.laz')
    # Extract all points with a LoD95% as NaN
    fc.split_laz(workspace+workflow_folder,'3D_M3C2_temp.laz')
    # Compute a second 3D-M3C2 on these points
    commande = cc.open_file(cc.open_file(cc.open_file(commande0,shift,workspace+Data_folder+filenames['pre_EQ_lidar']+'.laz'),shift,workspace+Data_folder+filenames['post_EQ_lidar']+'.laz'),shift,workspace+workflow_folder+'3D_M3C2_nan_temp.laz')
    cc.m3c2(commande,workspace+params_folder,params_file_m3c2_nan + '.txt')
    os.rename(workspace+Data_folder+list(filenames.values())[0]+'_M3C2.laz',workspace+workflow_folder+'3D_M3C2_nan_temp2.laz') 

    # Merge both the 3D M3C2 on NaN and the first 3D M3C2 
    commande = cc.open_file(cc.open_file(commande1,shift,workspace+workflow_folder+'3D_M3C2_split_temp.laz'),shift,workspace+workflow_folder+'3D_M3C2_nan_temp2.laz')
    cc.merge_clouds(commande)
    os.rename(workspace+workflow_folder+'3D_M3C2_split_temp'+'_MERGED.laz',workspace+workflow_folder+'3D_M3C2.laz')
    # Delete all temp files
    #os.remove(workspace+workflow_folder+'3D_M3C2_nan_d(10)_temp.laz')
    os.remove(workspace+workflow_folder+'3D_M3C2_split_temp.laz')
    os.remove(workspace+workflow_folder+'3D_M3C2_temp.laz')
    os.remove(workspace+workflow_folder+'3D_M3C2_nan_temp.laz')
    os.remove(workspace+workflow_folder+'3D_M3C2_nan_temp2.laz')
    
    # Compute LoD95% based on the t-statistics at 95% interval
    fc.compute_LoD(workspace+workflow_folder,'3D_M3C2',reg)
    # Extract significant changes (SC)
    fc.extract_SC(workspace+workflow_folder,'3D_M3C2.laz')
    
    
def Landslide_segmentation():
    # Extract erosion and deposition
    osf.open_folder(workspace+workflow_folder+segmentation_folder)
    for i in range(0,len(Extraction_folder)):
        osf.open_folder(workspace+workflow_folder+segmentation_folder+list(Extraction_folder.values())[i])
    fc.extract_erosion_deposition(workspace+workflow_folder,'Significant_changes_river_filtered.laz',segmentation_folder,Extraction_folder,Extraction_filenames)

    # Compute vertical M3C2
    for i in range(0,len(Extraction_folder)): 
        fc.writeExtraFields(workspace+workflow_folder+segmentation_folder+list(Extraction_folder.values())[i],list(Extraction_filenames.values())[i])
    
    osf.open_folder(workspace+workflow_folder)
    for i in range(0,len(Extraction_folder)):
        filenames['core_points'] = list(Extraction_filenames.values())[i]
        commande = cc.open_file(cc.open_file(cc.open_file(commande1,shift,workspace+Data_folder+filenames['pre_EQ_lidar']+'.laz'),shift,workspace+Data_folder+filenames['post_EQ_lidar']+'.laz'),shift,workspace+workflow_folder+segmentation_folder+list(Extraction_folder.values())[i]+filenames['core_points']+'.laz')
        cc.m3c2(commande,workspace+params_folder,params_file_Vm3c2 +'.txt')
        os.rename(workspace+Data_folder+list(filenames.values())[0]+'_M3C2.laz',workspace+workflow_folder+segmentation_folder+list(Extraction_folder.values())[i]+'Vertical_M3C2.laz')
    
    # Segmentation by connected components
    for i in range(0,len(Extraction_folder)):
        path_segmentation = workspace+workflow_folder+segmentation_folder+list(Extraction_folder.values())[i]
        osf.open_folder(path_segmentation+list(individual_outputs_folder.values())[i])
        fc.compute_SNR(path_segmentation,'Vertical_M3C2')
        df = fc.landslide_segmentation(path_segmentation,list(individual_outputs_folder.values())[i],list(individual_outputs_filenames.values())[i],shift,commande1,commande2,octree_level,min_point_per_component)
        # Write landslide information csv file
        path_res = workspace+workflow_folder+'res/'
        osf.open_folder(path_res)
        if i ==0:
            df.to_csv(path_res+'Landslide_source_infos.csv',sep=';')
        else:
            df.to_csv(path_res+'Landslide_deposits_infos.csv',sep=';')