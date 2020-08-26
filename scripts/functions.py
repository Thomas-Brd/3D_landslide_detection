# coding: utf-8
# Thomas Bernard
# Functions  
import pandas as pd

def split_SF(path,SF):
    """
    This function split the 3D M3C2 file
    path: path to the 3D M3C2 file
    SF: Name of the scalar field
    """
    df=pd.read_csv(path+'3D_M3C2_temp.asc',sep=',',header=0)
    df_nan=df[pd.isnull(df[SF])]
    df_nan = df_nan.fillna(0) # this line makes it possible to correctly read asc files on cloudcompare
    df = df[pd.notnull(df[SF])]
    df_nan.to_csv(path+'3D_M3C2_nan_temp.asc',sep=',',header=True,index=False)
    df.to_csv(path+'3D_M3C2_split_temp.asc',sep=',',header=True,index=False)
    
def add_suffix_and_columns(path,Extraction_folder,Extraction_filenames):
    normal_columns = ['Nx','Ny','Nz']
    for i in range(0,len(Extraction_folder)):
        df=pd.read_csv(path+list(Extraction_folder.values())[i]+list(Extraction_filenames.values())[i]+'.asc',sep=',',header=0)
        df = df.add_suffix('_3D')
        for ii in range(0,3):
            df.insert(ii+3,normal_columns[ii],0) # This is just to assure that all scalar fields would be read when opened in Cloudcompare
        df.to_csv(path+list(Extraction_folder.values())[i]+list(Extraction_filenames.values())[i]+'.asc',sep=',',header=True,index=False)
    
    