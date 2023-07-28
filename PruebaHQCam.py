from picamera import PiCamera
import picamera.array

cam = PiCamera()
cam.rotation = 180
# cam.resolution = (1920, 1080) # Uncomment if using a Pi Noir camera
cam.resolution = (2592, 1952) # Comment this line if using a Pi Noir camera
stream = picamera.array.PiRGBArray(cam)
cam.capture(stream, format='bgr', use_video_port=True)
original = stream.array

cv2.imwrite('original.png', original)