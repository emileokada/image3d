load mri
scanned_data = recon('./captures/');
Ds = smooth3(255*scanned_data.volume());
figure
isosurface(Ds,5)
rotate3d on
for x = -200:2:200
    campos([x,10,30])
    drawnow
end
% hiso = patch(isosurface(Ds,5),...
%    'FaceColor',[1,.75,.65],...
%    'EdgeColor','none');
% isonormals(Ds,hiso)
% view(35,30) 
% axis tight 
% daspect([1,1,1])
% lightangle(45,30);
% lighting gouraud
% hcap.AmbientStrength = 0.6;
% hiso.SpecularColorReflectance = 0;
% hiso.SpecularExponent = 50;