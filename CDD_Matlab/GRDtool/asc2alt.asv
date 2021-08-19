function topo=asc2alt()
% alt=asc2alt() : read DEM ascii files, and convert it into an .alt file
% for gridvisual

[filefel,pathname]=uigetfile('*.asc','Open a .asc file');
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

fclose(FEL);
% open the output file

fileout = strrep(filefel,'.asc','.alt');
fwriteGRD(topo,cellsize,fileout);

