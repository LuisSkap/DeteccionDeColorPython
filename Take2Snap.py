from picamera2 import Picamera2, Preview
from libcamera import controls
import time
import cv2

picam = Picamera2()
    
config = picam.create_still_configuration()
# config = picam.create_preview_configuration()
picam.configure(config)

picam.start_preview(Preview.QTGL)

picam.start()
time.sleep(0.5)
picam.capture_file("test-still.jpg")

time.sleep(0.5)

frame = cv2.imread('test-still.jpg')

cv2.imshow('test-python.jpg',frame)

#     camera = Picamera2()
#     camera.iso = 800
#     camera.sensor_mode=3
#     camera.resolution = (1024, 768)
#     camera.framerate=Fraction(1, 20)
#     camera.shutter_speed = 20000000
#     camera.iso = 800
#     camera.start_preview()
#     # Give the camera some time to adjust to conditions
#     time.sleep(20)
#     camera.capture('test.jpg')
    
    
