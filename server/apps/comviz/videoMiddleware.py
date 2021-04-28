#forked from https://github.com/electrocoder/Django-Webcam-Streaming/blob/master/camera.py
import cv2
import requests
import numpy as np
from apps.comviz.source.petsSegment import PetsSegmentor

# your Ip Webcam url
URL = 'http://192.168.0.xxx:8080/shot.jpg'

class VideoCamera(PetsSegmentor):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        super().__init__()
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        img_shape = np.array(image).shape[:-1]
        img = cv2.resize(image, self.img_size, interpolation = cv2.INTER_CUBIC)
        img = self.predictorWeb(img)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        image = cv2.resize(img, (512, 512), interpolation = cv2.INTER_CUBIC)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def get_frame_mobile(self):
        img_resp = requests.get(URL)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        image = cv2.imdecode(img_arr, -1)
        img_shape = np.array(image).shape[:-1]
        img = cv2.resize(image, self.img_size, interpolation = cv2.INTER_CUBIC)
        img = self.predictorWeb(img)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        image = cv2.resize(img, (512, 512), interpolation = cv2.INTER_CUBIC)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame_mobile()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')