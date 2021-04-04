import picamera

print ("taking pic")
with picamera.PiCamera() as camera:
	camera.resolution=(1280,720)
	camera.capture("test.jpg")
print ("pic taken")