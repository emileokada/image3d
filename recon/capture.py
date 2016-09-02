import cv2
import time

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

count = 0

while rval:
    if count % 30 == 0:
        cv2.imshow("preview", frame)
        cv2.imwrite(str(count)+"test.jpg",frame)
    rval, frame = vc.read()
    count = count + 1
    key = cv2.waitKey(20)
cv2.destroyWindow("preview")
