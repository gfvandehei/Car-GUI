import cv2
from threading import Thread, Lock
import time
from lib.common.commandable import Commandable
from enum import Enum

class CameraCommands(Enum):
    start = 1
    stop = 2


class Camera(Thread):

    def __init__(self, device_id: int = 0):
        super().__init__()
        self.device_id = device_id
        self.capture = cv2.VideoCapture(device_id)
        self.stopped_f = False
        self.listeners = []
        if not (self.capture.isOpened()):
            raise(AssertionError("The camera with id {} could not be opened".format(device_id)))

    def run(self):
        while self.capture.isOpened():
            if self.stopped_f:
                time.sleep(1)
                continue
            ret, frame = self.capture.read()
            for i in self.listeners:
                i.on_image(frame)
            time.sleep(1/60)

    def register_listener(self, observer):
        self.listeners.append(observer)

    def close(self):
        self.capture.release()

    def execute_command(self, command: int):
        if command == CameraCommands.start:
            # start camera
            self.stopped_f = False
            self.capture = cv2.VideoCapture(self.device_id)
        elif command == CameraCommands.stop:
            self.stopped_f = True
            self.close()


