from lib.sensors.basesensor import BaseSensor
from lib.sensors.camera_sensor.camera import Camera
from lib.common.tcpimageserver import TCPImageServer
import socket
from threading import Thread
import cv2
import pickle
import time
import json

class CameraSensor(BaseSensor):
    
    def __init__(self, port: int, *args):
        super().__init__(*args)
        self.mytype = 2
        self.end_f = False
        self.server_port = port

        self.my_server = TCPImageServer(self.server_port)
        self.camera = Camera()
        self.sensor_msg_thread = Thread(target= self.sensor_msg_thread)

        self.camera.register_listener(self)

    def on_image(self, image):
        # encode image
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        retval, buffer = cv2.imencode(".jpg", image, encode_param)
        img_as_text = pickle.dumps(buffer, 0)

        # pass image to server
        self.my_server.send_image(img_as_text)

    def sensor_msg_thread(self):
        while not self.end_f:
            #for i in self.split_image():
                #self.send_message(i)
            #time.sleep(1/60)
            message = {"data_addr": "localhost", "data_port": self.server_port}
            self.send_message(json.dumps(message).encode("utf-8"))
            time.sleep(1/60)

    def run(self):
        self.my_server.start()
        self.camera.start()
        self.sensor_msg_thread.start()
        super().run()