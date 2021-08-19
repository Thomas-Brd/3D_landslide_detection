function fwriteGRD(datas,scale,filename,varargin)
% fwriteGRD2(datas,scale,filename, bound)
% write a GRD file in the current directory. 
% scale is the horizontal resolution
% Bound is optional and corresponds to the true limits of the grid
% (generally obtained when opening a grd file with opengrd)

% Ouverture du fichier
IN=fopen(filename,'wb');
if IN==-1
   error('Unable to open the requested file')
end
[sizeX,sizeY]=size(datas);

if (nargin==3)
    xyzlohi(1)=0;
    xyzlohi(2)=(sizeX-1)*scale;
    xyzlohi(3)=0;
    xyzlohi(4)=(sizeY-1)*scale;
    xyzlohi(5)=min(min(datas));
    xyzlohi(6)=max(max(datas));
else
    xyzlohi=varargin{1};
end
 
% Ecriture de l'entete
fwrite(IN,'DSBB','char');
fwrite(IN,size(datas),'short');
fwrite(IN,xyzlohi(1),'double');
fwrite(IN,xyzlohi(2),'double');
fwrite(IN,xyzlohi(3),'double');
fwrite(IN,xyzlohi(4),'double');
fwrite(IN,xyzlohi(5),'double');
fwrite(IN,xyzlohi(6),'double');
% Ecriture des données
fwrite(IN,datas,'float');

fclose(IN);