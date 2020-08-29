# 3D landslide detection
This repository contains the dataset used in Bernard et al. (2020) and a jupyter notebook of the automatic workflow.

## Data 
Data used in Bernard et al.(2020) are located in the "Data/" folder. It contains:
* The modified LiDAR data from the study area (license: https://creativecommons.org/licenses/by/3.0/nz/)
* The landslide source and deposit informations 

## Workflow
The 3D landslide detection workflow can be execute from the jupyter notebook "3D_landslide_detection". The M3C2 parameters used can be found in the "Landslide_detection/" folder. The point cloud of the detected significant changes with fluvial erosion and sedimentation filtered is also provided.

The workflow uses the cloudcompare software (V2.11; http://www.cloudcompare.org/) and the M3C2 algorithm (Lague et al., 2013).