import time
from picamera2 import Picamera2, Preview
import os

os.environ["LIBCAMERA_LOG_LEVELS"] = "3"

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

preview_config = picam2.create_preview_configuration()
capture_config = picam2.create_still_configuration()
picam2.configure(capture_config)

picam2.start()
time.sleep(2)

picam2.switch_mode_and_capture_file(capture_config, "test_full.jpg")