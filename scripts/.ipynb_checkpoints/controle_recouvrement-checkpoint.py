# coding: utf-8
# Baptiste Feldmann
import numpy as np
import lidar_traitements as LT
import os
import glob
import matplotlib.pyplot as plt

workspace="G:/RENNES1/Loire_juin2019/04-QC/Recouvrement/"
shift="-436000 -6704000 0.0"
commande0="G:/RENNES1/BaptisteFeldmann/CloudCompare/cloudcompare -silent -c_export_fmt LAS -ext laz -auto_save OFF"
params_file="m3c2_params2.txt"
surface_water="G:/RENNES1/Loire_juin2019/05-Traitements/Loire_20190529_C2_thin_1m_surface_smooth_4m.laz"
filtre_dist_uncertainty=0.1

#LT.cloudcompare.c2c_files(commande0,workspace+"C2/","*C2_r_thin.laz",surface_water,shift,11,10)
#LT.cloudcompare.c2c_files(commande0,workspace+"C2_C3/","*.laz",surface_water,"Loire",10,10)

###------Compare C2-------#
##print("#------Compare C2------#")
##dossier="C2/"
##resultats=[]
##column_names=[]
##dictio_roots={21:["Moselle_20180324_01_L","-1_C2_r.laz"],51:["Moselle_20180324_02_L","-1_C2_r.laz"],66:["Moselle_20180325_01_L","-1_C2_r.laz"]}
##liste_keys=[21,51,66]
##print("Select pairs to test overlap...",end="\r")
##comparison=LT.calculs.select_pairs_overlap(workspace+dossier+"*_thin.laz",[21,2])
##print(" done !")
##print("Computing cloud comparison...")
##for i in comparison.keys() :
##    print("#===================#")
##    print("Line "+i+" :")
##    if int(i)<=liste_keys[0]:
##        rootname=dictio_roots[liste_keys[0]]
##    elif int(i)<=liste_keys[1]:
##        rootname=dictio_roots[liste_keys[1]]
##    else:
##        rootname=dictio_roots[liste_keys[2]]
##        
##    file1=rootname[0]+i+rootname[1]
##    corepts=file1[0:-4]+"_thin.laz"
##    
##    for c in comparison[i]:
##        print("Line "+c+"..",end='\r')
##        if int(c)<=liste_keys[0]:
##            rootname=dictio_roots[liste_keys[0]]
##        elif int(c)<=liste_keys[1]:
##            rootname=dictio_roots[liste_keys[1]]
##        else:
##            rootname=dictio_roots[liste_keys[2]]
##            
##        file2=rootname[0]+c+rootname[1]
##        file_result=corepts[0:-4]+"_m3c2_"+i+"and"+c+".laz"
##        commande=LT.cloudcompare.open_file(LT.cloudcompare.open_file(LT.cloudcompare.open_file(commande0,shift,workspace+dossier+file1),
##                                                                     shift,workspace+dossier+file2),shift,workspace+dossier+corepts)
##        LT.cloudcompare.m3c2(commande,workspace+params_file)
##        new_file1=LT.cloudcompare.last_file(workspace+dossier+corepts[0:-4]+"_20*.laz",file_result)
##        new_file=LT.cloudcompare.last_file(workspace+dossier+file1[0:-4]+"_20*.laz")
##        os.remove(new_file)
##        new_file=LT.cloudcompare.last_file(workspace+dossier+file2[0:-4]+"_20*.laz")
##        os.remove(new_file)
##        
##        tab,names=LT.lastools.readLAS(workspace+dossier+file_result,extra_field=True)
##        #select=tab[:,np.where(names=='c2c_absolute_distances_(z)')[0][0]]>0.25
##        #tab2=tab[select,:]
##        tab2=np.copy(tab)
##        tab3=tab2[np.logical_not(np.isnan(tab2[:,np.where(names=="distance_uncertainty")[0][0]])),:]
##        select=tab3[:,np.where(names=="distance_uncertainty")[0][0]]<filtre_dist_uncertainty
##        tab4=tab3[select,:]
##        m3c2_dist=tab4[np.logical_not(np.isnan(tab4[:,np.where(names=="m3c2_distance")[0][0]])),np.where(names=="m3c2_distance")[0][0]]
##        
##        if len(m3c2_dist)>100:
##            column_names+=[i+"_"+c]
##            resultats+=[[np.mean(m3c2_dist),np.std(m3c2_dist)]]
##    print("done !")
##
##column_names=np.reshape(np.array(column_names),(len(column_names),1))
##result=np.concatenate((column_names,np.round_(np.array(resultats),3)),axis=1)
##np.savetxt(workspace+dossier+"save_results.txt",result,fmt='%s',delimiter=";",header="Comparaison;moyenne (m);ecart-type (m)")
##print("#=====================#\n")
###=============================#


#------Compare C3-------#
##print("#------Compare C3------#")
##dossier="C3/"
##resultats=[]
##column_names=[]
##dictio_roots={26:["Loire_Univ-Tours_S01_20190529_Loire-Univ-Tours_L","_C3_r.laz"],51:["Moselle_20180324_02_L","_C3_r.laz"],66:["Moselle_20180325_01_L","_C3_r.laz"]}
##liste_keys=[26]
##print("Select pairs to test overlap...",end="\r")
##comparison=LT.calculs.select_pairs_overlap(workspace+dossier+"*_thin.laz",[len(dictio_roots[26][0]),2])
##print(" done !")
##print(comparison)
##print("Computing cloud comparison...")
##for i in comparison.keys() :
##    print("#===================#")
##    print("Line "+i+" :")
##    if int(i)<=liste_keys[0]:
##        rootname=dictio_roots[liste_keys[0]]
##    elif int(i)<=liste_keys[1]:
##        rootname=dictio_roots[liste_keys[1]]
##    else:
##        rootname=dictio_roots[liste_keys[2]]
##
##    file1=rootname[0]+i+rootname[1]
##    corepts=file1[0:-4]+"_thin.laz"
##    
##    for c in comparison[i]:
##        print("Line "+c+"..",end='\r')
##        if int(c)<=liste_keys[0]:
##            rootname=dictio_roots[liste_keys[0]]
##        elif int(c)<=liste_keys[1]:
##            rootname=dictio_roots[liste_keys[1]]
##        else:
##            rootname=dictio_roots[liste_keys[2]]
##        
##        file2=rootname[0]+c+rootname[1]
##        file_result=corepts[0:-4]+"_m3c2_"+i+"and"+c+".laz"
##        commande=LT.cloudcompare.open_file(LT.cloudcompare.open_file(LT.cloudcompare.open_file(commande0,shift,workspace+dossier+file1),
##                                                                     shift,workspace+dossier+file2),shift,workspace+dossier+corepts)
##        LT.cloudcompare.m3c2(commande,workspace+params_file)
##        new_file1=LT.cloudcompare.last_file(workspace+dossier+corepts[0:-4]+"_20*.laz",file_result)
##        new_file=LT.cloudcompare.last_file(workspace+dossier+file1[0:-4]+"_20*.laz")
##        os.remove(new_file)
##        new_file=LT.cloudcompare.last_file(workspace+dossier+file2[0:-4]+"_20*.laz")
##        os.remove(new_file)
##        
##        tab,metadata=LT.lastools.readLAS(workspace+dossier+file_result,extra_field=True)
##        names=metadata['col_names']
##        #select=tab[:,np.where(names=='c2c_absolute_distances_(z)')[0][0]]>0.25
##        #tab2=tab[select,:]
##        tab2=np.copy(tab)
##        tab3=tab2[np.logical_not(np.isnan(tab2[:,names.index("distance_uncertainty")])),:]
##        select=tab3[:,names.index("distance_uncertainty")]<filtre_dist_uncertainty
##        tab4=tab3[select,:]
##        tab5=tab4[np.logical_not(np.isnan(tab4[:,names.index("m3c2_distance")])),names.index("m3c2_distance")]
##        select=np.logical_and(tab5>-2,tab5<2)
##
##        m3c2_dist=tab5[select]
##        if len(m3c2_dist)>100:
##            column_names+=[i+"_"+c]
##            resultats+=[[np.mean(m3c2_dist),np.std(m3c2_dist)]]
##    print("done !")
##
##column_names=np.reshape(np.array(column_names),(len(column_names),1))
##result=np.concatenate((column_names,np.round_(np.array(resultats),3)),axis=1)
##np.savetxt(workspace+dossier+"save_results.txt",result,fmt='%s',delimiter=";",header="Comparaison;moyenne (m);ecart-type (m)")
##print("#=====================#\n")
#=============================#
##
#-------Compare C2_C3------#
##print("#-----Compare C2-C3 --------#")
##dossier="C2_C3/"
##liste_files=glob.glob(workspace+dossier+"*_C2_r.laz")
##column_names=[]
##resultats=[]
##print("Computing cloud comparison...")
##for f in liste_files:
##    print("#===================#")
##    file1=os.path.split(f)[1]
##    print(file1)
##    number=file1[48:50]
##    file2=file1[0:-9]+"_C3_r.laz"
##    corepts=file1[0:-4]+"_thin.laz"
##
##    file_result=corepts[0:-4]+"_m3c2_C2C3.laz"
##    commande=LT.cloudcompare.open_file(LT.cloudcompare.open_file(LT.cloudcompare.open_file(commande0,shift,workspace+dossier+file1),
##                                                                 shift,workspace+"C2_C3/"+file2),shift,workspace+dossier+corepts)
##    LT.cloudcompare.m3c2(commande,workspace+params_file)
##    new_file1=LT.cloudcompare.last_file(workspace+dossier+corepts[0:-4]+"_20*.laz",file_result)
##    new_file=LT.cloudcompare.last_file(workspace+dossier+file1[0:-4]+"_20*.laz")
##    os.remove(new_file)
##    new_file=LT.cloudcompare.last_file(workspace+dossier+file2[0:-4]+"_20*.laz")
##    os.remove(new_file)
##    
##    tab,metadata=LT.lastools.readLAS(workspace+dossier+file_result,extra_field=True)
##    names=metadata['col_names']
##    #select=tab[:,np.where(names=='c2c_absolute_distances_(z)')[0][0]]>0.25
##    #tab2=tab[select,:]
##    tab2=np.copy(tab)
##    tab3=tab2[np.logical_not(np.isnan(tab2[:,names.index("distance_uncertainty")])),:]
##    select=tab3[:,names.index("distance_uncertainty")]<filtre_dist_uncertainty
##    tab4=tab3[select,:]
##    tab5=tab4[np.logical_not(np.isnan(tab4[:,names.index("m3c2_distance")])),names.index("m3c2_distance")]
##    select=np.logical_and(tab5<2,tab5>-2)
##    m3c2_dist=tab5[select]
##    
##    if len(m3c2_dist)>100:
##        column_names+=[number]
##        resultats+=[[np.mean(m3c2_dist),np.std(m3c2_dist)]]
##
##column_names=np.reshape(np.array(column_names),(len(column_names),1))
##result=np.concatenate((column_names,np.round_(np.array(resultats),3)),axis=1)
##np.savetxt(workspace+dossier+"save_results.txt",result,fmt='%s',delimiter=";",header="Comparaison;moyenne (m);ecart-type (m)")
##print("#=====================#\n")
#========================#

from joblib import Parallel,delayed

workspace="G:/RENNES1/Loire_juin2019/04-QC/Recouvrement/C2_C3/"
liste=glob.glob(workspace+"*_m3c2_C2C3_C2C.laz")
liste_noms=[os.path.split(i)[1] for i in liste]

##def func(workspace,filename,distance_filter):
##    number=filename[48:50]
##    #number=filename[-11:-4]
##
##    tab,metadata=LT.lastools.readLAS(workspace+filename,extra_field=True)
##    names=metadata['col_names']
##    select=tab[:,names.index('c2c_absolute_distances_(z)')]>0.25
##    tab2=tab[select,:]
##    #tab2=np.copy(tab)
##    tab3=tab2[np.logical_not(np.isnan(tab2[:,names.index("distance_uncertainty")])),:]
##    select=tab3[:,names.index("distance_uncertainty")]<distance_filter
##    tab4=tab3[select,:]
##    tab5=tab4[np.logical_not(np.isnan(tab4[:,names.index("m3c2_distance")])),names.index("m3c2_distance")]
##    select=np.abs(tab5)<1
##    m3c2_dist=tab5[select]
##        
##    if len(m3c2_dist)>100:
##        #column_names=number[0:2]+"_"+number[-2::]
##        line_select=np.unique(np.random.randint(0,len(m3c2_dist),int(0.5*len(m3c2_dist))))
##        column_names=number
##        resultats=m3c2_dist[line_select]
##        select=np.arange(0,len(resultats),3)
##        return [column_names,resultats[select]]
##
##
##result=Parallel(n_jobs=10, verbose=2)(delayed(func)(workspace,i,filtre_dist_uncertainty) for i in liste_noms)
##
##column_names=[]
##data=[]
##for i in result:
##    if i!=None:
##        column_names+=[i[0]]
##        data+=list(i[1])
##
##np.savez_compressed(workspace+"save_results_data.npz",data)


f=np.load(workspace+"save_results_data.npz")
#f,names=LT.lastools.readLAS(workspace+"Bathy_altitude_L93_m3c2_bis.laz",extra_field=True)
#tab=f[:,np.where(names=="m3c2_distance")[0][0]]
tab=f[f.files[0]]

print(np.mean(tab))
print(np.std(tab))

plt.figure(1)
plt.xlabel("Distance M3C2 (en cm)")
plt.ylabel("Fréquence")
plt.title('Histogramme des écarts en altitude\npour les données du canal vert')
plt.hist(tab*100,bins=50,range=(-25,25),edgecolor='white')
plt.ticklabel_format(axis="y",style='sci',scilimits=(0,0))
#plt.text(x=-30,y=3000,s="Moyenne : -9cm\nEcart-type : 5.5cm")
plt.savefig(workspace+"figure_data.png",dpi=150)




