function []=alt2asc()
% []=alt2asc() : transform a .alt (or .grd) file into an ascii file for taudem analysis

[filegrd,pathname]=uigetfile('*.alt','Open a .alt file');
eval(['cd ' pathname]);

[scale,alt]=fopengrd(filegrd);

fileout=strrep(filegrd,'.alt','.asc');

OUT=fopen(fileout,'wt');
alt=alt';
[nbcols,nbrows]=size(alt);

ind=find(alt<0);
alt(ind)=-1;

% Header
% ncols 480
% nrows 450
% xllcorner 378923
% yllcorner 4072345
% cellsize 30
% nodata_value -32768

fprintf(OUT,'ncols %i\n',nbcols);
fprintf(OUT,'nrows %i\n',nbrows);
fprintf(OUT,'xllcorner %i\n',0);
fprintf(OUT,'yllcorner %i\n',0);
fprintf(OUT,'cellsize %i\n',scale);
fprintf(OUT,'nodata_value %i\n',-1);

%for i=1:nbcols
    %for j=1:nbrows
fprintf(OUT,'%f ',alt)
fclose(OUT);



