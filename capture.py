import parallel
import pygame
import pygame.camera
import time

#Initialize parallel port
port = parallel.Parallel()

#Initialize webcam
pygame.camera.init()
cameras = pygame.camera.list_cameras()
webcam = pygame.camera.Camera(cameras[0])
webcam.start()


counter = -2
current_status = True
prev_status = True

port.setData(255)
img = webcam.get_image()
pygame.image.save(img, "test.jpg")
time.sleep(1.00)

while counter<60:
    time.sleep(0.01)
    prev_status = current_status
    current_status = port.getInAcknowledge()
    if not current_status and prev_status:
	counter = counter + 1
	print counter
	img = webcam.get_image()
	if counter > 0:
	    pygame.image.save(img, "pictures/"+str(counter)+".jpg")

port.setData(0)
