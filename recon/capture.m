cam = webcam(2);
imgs = cell(20);
for i = 1:20
    imgs{i} = snapshot(cam);
    pause(0.4)
end
H = fspecial('disk',4);
for i = 1:20
    temp_img = im2bw(imgs{i},0.5)';
    imwrite(imfilter(temp_img(1:1080,:),H,'replicate'),['./captures/',num2str(i),'.jpg']);
end

clear('cam');