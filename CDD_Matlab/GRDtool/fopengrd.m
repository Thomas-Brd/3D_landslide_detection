function [scaleGRD,matGRD,xyzlohi]=fopenGRD(filename)
% [scaleGRD,matGRD]=fopenGRD('filename');
% OPEN a file in GRD format. Store the datas in the matGRD matrice
% Store the scale (meters) in scaleGRD

IN=fopen(filename,'rb');
if IN==-1
   error('Unable to open the requested file')
end

% Lecture de l'entête
entete=char(fread(IN,[1 4],'char'));
%if (~(strcmp('DSBB',entete)))
%   error('This file is not a GRD file')
%end

sizeX=fread(IN,1,'short');
sizeY=fread(IN,1,'short');
xyzlohi=fread(IN,6,'double');

% Calcul de l'echelle
scaleGRD=(xyzlohi(2)-xyzlohi(1))/(sizeX-1);
nData=sizeX*sizeY;

% Lecture des données

matGRD=fread(IN,[sizeX sizeY],'float');

fclose(IN);