function data=openrtg_g()
% data=openrtg_g : ouverture interactive d'un fichier rtg de rivertools de type rtg

[filertg,pathname]=uigetfile('*.rtg','Open a Rivertools .rtg file');

eval(['cd ' pathname]);

% Open the .rti file

%filerti = strrep(filertg,'_area.rtg','.rti');
[filerti,pathname]=uigetfile('*.rti','Open a Rivertools .rti file');


RTI=fopen(filerti,'rt');
RTG=fopen(filertg,'rb');

% Find the size of the file in the rti file

for i=1:11
   line=fgets(RTI);
end
% 20 caractère avant le nombre de colonnes
fgets(RTI,20);
nbcol=fscanf(RTI,'%d',[1,1])
fgets(RTI);
fgets(RTI,20);
nbrow=fscanf(RTI,'%d',[1,1])

% Get the entire grid data

data=fread(RTG,[nbcol,nbrow],'float');

% Close the files

fclose(RTI);
fclose(RTG);

% Draw the data

%plot2d(data,1);


