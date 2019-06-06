import time
import picamera
with picamera.PiCamera() as camera:
    camera.vflip = true
    camera.resolution = (1080,720)
    camera.start_preview()
    try:
        for i, filename in enumerate(
                camera.capture_continuous('image{counter:02d}.jpg')):
            print(filename)
            time.sleep(1/fps)
            if i == nimgs:
                break
    finally:
        camera.stop_preview()