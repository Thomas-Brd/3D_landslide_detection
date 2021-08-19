function writeGRD2(datas,scale)
% writeGRD(datas,scale,name)
% write a GRD file in the current directory. Filename prompt. 

% Ouverture du fichier
[filename,pathname]=uiputfile('Fichier GRD à ecrire','*.*');
eval(['cd ' pathname]);

IN=fopen(filename,'wb');
if IN==-1
   error('Unable to open the requested file')
end
datas=fliplr(datas);
[sizeX,sizeY]=size(datas);
minima=min(min(datas));
maxima=max(max(datas));
if ((maxima==minima) & (maxima>0))
   minima=0;
end
% Ecriture de l'entete
fwrite(IN,'DSBB','char');
fwrite(IN,size(datas),'short');
fwrite(IN,0,'double');
fwrite(IN,sizeX*scale,'double');
fwrite(IN,0,'double');
fwrite(IN,sizeY*scale,'double');
fwrite(IN,minima,'double');
fwrite(IN,maxima,'double');

% Ecriture des données
fwrite(IN,datas,'float');

fclose(IN);