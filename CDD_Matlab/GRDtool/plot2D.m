function plot2D(datas,pos)
% plot2D(2dmatrix)
% Plot in 2 dimension the values of a 2D matrix, with color nuances
% Pos is the position of the colorbar : 0 : no colorbar, 1 : horizontale,
% 2:verticale
datas=flipud(datas);
[sizeX,sizeY]=size(datas);

pcolor(datas)
shading interp
colormap(hot)
axis equal
%axis ij
axis([1 sizeY 1 sizeX])
if (pos==1)
   colorbar('horiz');
elseif (pos==2)
   colorbar;
end
   

