function writeGRD(datas,scale,varargin)
% writeGRD(datas,scale)
% write a GRD file in the current directory. Filename prompt. 

% Ouverture du fichier
[filename,pathname]=uiputfile('Fichier GRD à ecrire','*.*');
%eval(['cd ' pathname]);

if (nargin==2)
    fwritegrd(datas,scale,filename);
else
    xyzlohi=varargin{1};
    fwritegrd(datas,scale,filename,xyzlohi);
end