function [data,res,coord]=openbil(option,filebil)
% [data,res,coord]=openbil(plotdata): ouverture interactive d'un fichier image .bil, avec fichiers compagnons
% .hdr, .sfx et .blw
% Option = 0: affichage, 1 : pas d'affichage, 2 : pas d'affichage et ecriture d'un fichier grd.
% Pas d'option -> affichage sans ecriture d'un fichier grd
% le nom de l'image suivi de .alt
% filename: optionel, permet d'entrer directement le nom du fichier .bil
% data = matrix containig the image
% res = spatial resolution
% coord = coordinates of the south-east corner in the projection (geographic or cartographic)

if nargin==0, option=0; end
if nargin==1
    [filebil,pathname]=uigetfile('*.bil','Open an image .bil file');
    eval(['cd ' pathname]);
end
% Open the .hdr file

filehdr = strrep(filebil,'.bil','.hdr');
%[filehdr,pathname]=uigetfile('*.hdr','Open an .hdr file');


HDR=fopen(filehdr,'rt');
BIL=fopen(filebil,'rb');

% Analyse of the HDR file
% Structure d'un fichier HDR
% BYTEORDER      I    
% LAYOUT       BIL
% NROWS         9626
% NCOLS         5156
% NBANDS        1       % a verifier pour etre sur qu'il n'y a qu'une bande
% NBITS         16      % a lire pour savoir le format d'import
% BANDROWBYTES         10312
% TOTALROWBYTES        10312
% BANDGAPBYTES         0

byteorder=fgets(HDR);
layout=fgets(HDR);
linerow=fgets(HDR);
linecol=fgets(HDR);
lineband=fgets(HDR);
linebits=fgets(HDR);
nbrow=sscanf(linerow,'NROWS %i');
nbcol=sscanf(linecol,'NCOLS %i');
nbands=sscanf(lineband,'NBANDS %i');
nbits=sscanf(linebits,'NBITS %i');
if (nbands>1)
    fclose(HDR);
    fclose(BIL);
    disp(['BIL file has ' int2str(nbands) ' bands. Exiting import']);
    return;
end
fclose(HDR);

% Lecture du fichier .stx contenant les statistiques du fichier
filestx = strrep(filebil,'.bil','.stx');
[mind,maxd,meand,stdd]=textread(filestx,'1 %f %f %f %f');

% Lecture du fichier .blw contenant les coordonnees du coin sud-est de l'image ainsi
% que la resolution
fileblw = strrep(filebil,'.bil','.blw');
BLW=fopen(fileblw,'rt');
if (BLW==-1)
   disp('Impossible ouvrir le fichier de coordonnees');
   res=0;coord=0;
else
    temp=fscanf(BLW,'%f');
    fclose(BLW);
    res(1)=temp(1);res(2)=temp(4);coord(1)=temp(5);coord(2)=temp(6);
    if (res(1)~=res(2))
        disp('Attention resolution en x et y differente')
        disp(abs(res));
    else
        res=abs(res(1));
    end
    disp(['Resolution: ' num2str(res), '. Coordinates of the south-east corner:' num2str(coord)])
end

% Display file properties
disp(['BIL file has ' int2str(nbrow) ' rows and ' int2str(nbcol) ' columns'])
switch nbits
case 8
    bitcode='int8';
case 16
    bitcode='int16';
case 32
    bitcode='float32';
case 64
    bitcode='double';
end    
disp(['Records coded in ' bitcode])
%disp(['Statistics as in stx file: Min: ' num2str(mind) ', Max: ' num2str(maxd) ...
%        ', Mean: ' num2str(meand) ', Std: ' num2str(stdd)]);

% reading the BIL file

data=fread(BIL,[nbcol,nbrow],bitcode);
if (nbcol*nbrow<1e6)
    mind=min(min(data));
    maxd=max(max(data));
    meand=mean(mean(data));
    stdd=std(std(data));
    disp(['Computed statistics : Min: ' num2str(mind) ', Max: ' num2str(maxd) ...
        ', Mean: ' num2str(meand) ', Std: ' num2str(stdd)]);
end

% Coordinates and resolution


% Close the files
fclose(BIL);

% Draw the data
if (option==0)
    plot2d(data,1);
end

% Write a grd file
if (option>1)
    grdname=strrep(filebil,'.bil','.alt');
    %data=fliplr(data);
    fwritegrd(data',abs(res(1)),grdname);
end
    
