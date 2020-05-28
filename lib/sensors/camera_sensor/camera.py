import cv2
from threading import Thread
import time


class Camera(Thread):

    def __init__(self, device_id: int = 0):
        super().__init__()
        self.capture = cv2.VideoCapture(device_id)
        self.listeners = []
        if not (self.capture.isOpened()):
            raise(AssertionError("The camera with id {} could not be opened".format(device_id)))

    def run(self):
        while self.capture.isOpened():
            ret, frame = self.capture.read()
            for i in self.listeners:
                i.on_image(frame)
            time.sleep(1/60)

    def register_listener(self, observer):
        self.listeners.append(observer)

    def close(self):
        self.capture.release()

