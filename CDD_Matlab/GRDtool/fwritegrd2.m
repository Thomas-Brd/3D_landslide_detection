function fwriteGRD(datas,scale,coord,filename)
% fwriteGRD2(datas,scale,filename)
% write a GRD file in the current directory. 
% scale is the horizontal resolution
% coord is the location of the south-east corner

% Ouverture du fichier
IN=fopen(filename,'wb');
if IN==-1
   error('Unable to open the requested file')
end
[sizeX,sizeY]=size(datas);
% Ecriture de l'entete
fwrite(IN,'DSBB','char');
fwrite(IN,size(datas),'short');
fwrite(IN,coord(1),'double');
fwrite(IN,sizeX*scale,'double');
fwrite(IN,coord(2),'double');
fwrite(IN,sizeY*scale,'double');
fwrite(IN,min(min(datas)),'double');
fwrite(IN,max(max(datas)),'double');

% Ecriture des données
fwrite(IN,datas,'float');

fclose(IN);