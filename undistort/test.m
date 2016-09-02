images = imageSet(fullfile('./captures/'));
[imagePoints, boardSize] = detectCheckerboardPoints(images.ImageLocation);
squareSize = 29;
worldPoints = generateCheckerboardPoints(boardSize, squareSize);
cameraParams = estimateCameraParameters(imagePoints, worldPoints);
I = images.read(1);
J1 = undistortImage(I, cameraParams);
figure; imshowpair(I, J1, 'montage');
title('Original Image (left) vs. Corrected Image (right)');

J2 = undistortImage(I, cameraParams, 'OutputView', 'full');
figure; imshow(J2);
title('Full Output View');