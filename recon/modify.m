im_dir = './pictures/';
files = get_files(im_dir);
[increments, ~] = size(obj.files);
H = fspecial('disk',3);
for  i = 1:1
    img = double(...
        rgb2gray(imread([im_dir,files{i,1}])))/255;
    temp_img = im2bw(img,0.5);
    img1 = imfilter(temp_img,H,'replicate');
    imshow(img1);
end
