% opengrd : ouverture interactive d'un fichier grd.
% Le resultat est stock� dans scale, et altitude

[filename,pathname]=uigetfile('*.*','Open a GRD file');

%eval(['cd ' pathname]);

[scale,altitude,bound]=fopengrd([pathname filename]);