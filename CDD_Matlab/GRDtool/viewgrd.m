% viewGRD : affichage en 3D d'un fichier GRD
% OPEN a file in GRD format. Store the datas in the matGRD matrice
% Store the scale in meters in scaleGRD
% Generate a figure with datas in 3D

ls
filename=input('Name of the GRD file :','s');
matname=input('Name of the matrix :','s');

IN=fopen(filename,'rb');
if IN==0
   error('Unable to open the requested file')
end

% Lecture de l'entête
entete=char(fread(IN,[1 4],'char'));
if (~(strcmp('DSBB',entete)))
   error('This file is not a GRD file')
end

sizeX=fread(IN,1,'short')
sizeY=fread(IN,1,'short')
xyzlohi=fread(IN,6,'double');

% Calcul de l'echelle
scaleGRD=(xyzlohi(2)-xyzlohi(1))/sizeX
nData=sizeX*sizeY;
altGRD=zeros(sizeX,sizeY);

% Lecture des données
altGRD=fread(IN,[sizeX sizeY],'float');
eval([matname,'=altGRD;']);

% VISUALISATION
surfl(alt)
shading interp
colormap(pink)
axis([0 sizeX 0 sizeY 0 4*max(max(altGRD))])
view([45 45])
title(filename)

% CLEAR
fclose(IN);
clear altGRD;