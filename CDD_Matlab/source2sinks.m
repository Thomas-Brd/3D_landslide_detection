clear all; close all;
addpath(genpath('topotoolbox-master/'),'-end');addpath(genpath('GRDtool/'),'-end');

%% Load datasets
DEM = GRIDobj('tif/MNT.tif');
M_S = GRIDobj('tif/mask_sources.tif');
M_D = GRIDobj('tif/mask_depots.tif');M_D.Z(M_D.Z>0)=1;
Id_S = GRIDobj('tif/id_sources.tif');
Id_D = GRIDobj('tif/id_depots.tif');

%% Compute hydro-topo properties
T = fillsinks(DEM);
% Compute slope
S = gradient8(T);
% Compute flow direction
FD = FLOWobj(T,'mex',true); % single-flow
% Compute drainage area
A  = flowacc(FD);A.Z=A.Z.*DEM.cellsize.^2;

%% Compute distance from sources to the closests deposits along flowpaths
dist=zeros(max(max(Id_S.Z)),1);indtoremove=find(isnan(M_D.Z)==1 | M_D.Z~=1);
parfor i=1:max(max(Id_S.Z))
    i
    IX=find(Id_S.Z==i); % Indices of the pixels associated to the i-th source
    D = flowdistance(FD,IX,'downstream'); % Downstream distances
    D.Z(indtoremove)=NaN; % Remove from distances the location not corresponding to deposits
    [dist(i), temp{i} ] = minmat(D.Z) % Compute the minimum distance and the associated location
    Id_S2D(i)=Id_D.Z(temp{i}(1),temp{i}(2)); % Compute the Id of the associated deposit
end

% Convert the position to an ij matrix
for i=1:max(max(Id_S.Z));ij(i,1)=temp{i}(1);ij(i,2)=temp{i}(2);end

% Export results
writematrix(dist,'distance.txt')
writematrix(ij,'ijpixelD.txt')
writematrix(Id_S2D,'Id_S2D.txt')
