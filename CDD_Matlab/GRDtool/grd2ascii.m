% grd2ascii : transform a grd file in row-column ascii file for GENESIS II
% Script de transformation d'un fichier GRD en fichier ascii ligne-colonne pour GENESISII
% en attendant d'avoir un format binaire decent !
disp('Conversion GRD -> ASCII lignes colonnes')
opengrd;

fileascii=[filename '.txt'];
OUT=fopen(fileascii,'wt');
datas=altitude;

[sizeX,sizeY]=size(datas);
maximum=max(max(datas));

% Scaling pour GENESIS II, pour atteindre 1000 m
datas=1000/maximum*datas;
for i=1:sizeX
   for j=1:sizeY
      fprintf(OUT,'%f\t',datas(i,j));
   end
   fprintf(OUT,'\n');
end
fclose(OUT);
clear all;