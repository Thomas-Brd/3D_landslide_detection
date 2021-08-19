function topo=asc2sa()
% alt=asc2grd() : read several ascii files from TAUDEM software, and
% convert it into a column data file
% currently read : fel : pit filled elevation data, sd8 : D8 slopes, ad8 : D8area
%                   slp : Dinf slopes, sca : Dinf area, src : basin number


[filefel,pathname]=uigetfile('*fel.asc','Open a fel.asc file');
eval(['cd ' pathname]);

% get the sizes and scale
% ncols 480
% nrows 450
% xllcorner 378923
% yllcorner 4072345
% cellsize 30
% nodata_value -32768

FEL=fopen(filefel,'rt');

linecols=fgets(FEL);
linerows=fgets(FEL);
fgets(FEL);fgets(FEL);
linesize=fgets(FEL);
linenodata=fgets(FEL);
nbrow=sscanf(lower(linerows),'nrows %i')
nbcol=sscanf(lower(linecols),'ncols %i')
cellsize=sscanf(lower(linesize),'cellsize %i')
nodata=sscanf(lower(linenodata),'nodata_value %i')

% read the elevation

topo=fscanf(FEL,'%f',[nbcol,nbrow]);
ind=find(topo==-9999);
topo(ind)=-1;
plot2d(topo,1)
fseek(FEL,0,-1);
movetoline(FEL);

% open the output file

fileout = strrep(filefel,'fel.asc','_tarb.dat');
OUT=fopen(fileout,'wt');

% Open the various files and go to the first line

fileSD8 = strrep(filefel,'fel.asc','sd8.asc');
fileAD8 = strrep(filefel,'fel.asc','ad8.asc');
fileSLP = strrep(filefel,'fel.asc','slp.asc');
fileSCA = strrep(filefel,'fel.asc','sca.asc');
fileBASIN=strrep(filefel,'fel.asc','w.asc');

SD8=fopen(fileSD8,'rt'); AD8=fopen(fileAD8,'rt'); SLP=fopen(fileSLP,'rt'); SCA=fopen(fileSCA,'rt');
BASIN=fopen(fileBASIN,'rt');
movetoline(SD8);movetoline(AD8);movetoline(SLP);movetoline(SCA);movetoline(BASIN);

% to avoid to store large grid, read directly from file
fprintf(OUT,'Elevation\t AD8\t SD8\t ADinf\t SDinf\t Basin\n');
for i=1:nbcol*nbrow
    alt=fscanf(FEL,'%f',1); aireD8=fscanf(AD8,'%f',1); slopeD8=fscanf(SD8,'%f',1);
    aireDinf=fscanf(SCA,'%f',1);slopeDinf=fscanf(SLP,'%f',1);val=fscanf(BASIN,'%f',1);
    if ((alt>=0) & (aireD8>0) & (aireDinf>0) & (val>0))
        fprintf(OUT,'%f\t %f\t %f\t %f\t %f\t %f\n',alt,aireD8,slopeD8,aireDinf,slopeDinf,val);
    end
end

% Close all files
fclose(SD8); fclose(AD8); fclose(SLP); fclose(SCA); fclose(FEL); fclose(OUT);


%Functions
function []=movetoline(fid)
% movetoline : move of 6 lines to the beginning of the data record
fgets(fid);fgets(fid);fgets(fid);fgets(fid);fgets(fid);fgets(fid);
