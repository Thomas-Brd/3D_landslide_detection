function iwriteGRD(datas,scale,filename)
% writeGRD(datas,scale,'filename')
% write a GRD file in the current directory. 

% Ouverture du fichier
%[filename,pathname]=uiputfile('Fichier GRD à ecrire','*.*');
%eval(['cd ' pathname]);

IN=fopen(filename,'wb');
if IN==-1
   error('Unable to open the requested file')
end
[sizeX,sizeY]=size(datas);
% Ecriture de l'entete
fwrite(IN,'DSBB','char');
fwrite(IN,size(datas),'short');
fwrite(IN,0,'double');
fwrite(IN,sizeX*scale,'double');
fwrite(IN,0,'double');
fwrite(IN,sizeY*scale,'double');
fwrite(IN,min(min(datas)),'double');
fwrite(IN,max(max(datas)),'double');

% Ecriture des données
fwrite(IN,datas,'float');

fclose(IN);