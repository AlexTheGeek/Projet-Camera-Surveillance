import picamera

camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.capture('exemple.jpg')

print("Photo prise")
