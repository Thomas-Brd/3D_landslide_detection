% view2DGRD : affiche en 2D un fichier GRD
% OPEN a file in GRD format. Store the datas in the matGRD matrice
% Store the scale in meters in scaleGRD

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
plot2d(altGRD)
title(filename)

% CLEAR
fclose(IN);
clear altGRD;