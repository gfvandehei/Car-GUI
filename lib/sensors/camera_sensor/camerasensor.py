from lib.sensors.basesensor import BaseSensor
from lib.sensors.camera_sensor.camera import Camera, CameraCommands
from lib.common.tcpimageserver import TCPImageServer
import socket
from threading import Thread
import cv2
import pickle
import time
import struct
import json
from lib.common.commandable import Commandable

"""
CameraSensor: The base remote sensor class, allowing viewing of camera feed,
              and control of camera
"""
class CameraSensor(BaseSensor, Commandable):
    
    def __init__(self, port: int, *args):
        super().__init__(*args)
        self.mytype = 2
        self.end_f = False
        self.server_port = port
        self.paused_f = False
        # create server for image clients to attach to
        self.my_server = TCPImageServer(self.server_port)
        # create camera to access system camera
        self.camera = Camera()
        # create thread to breadcast self: TODO: add class that does this
        self.sensor_msg_t = Thread(target= self.sensor_msg_thread)
        # listen for images from camera
        self.camera.register_listener(self)
        # listen for commands from tcp clients
        self.my_server.register_commandable(self)

    """
    on_image: handles what to do when an image is received an image is thrown through the callback
    """
    def on_image(self, image):
        # encode image
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        retval, buffer = cv2.imencode(".jpg", image, encode_param)
        img_as_text = pickle.dumps(buffer, 0)

        # pass image to server
        self.my_server.send_image(img_as_text)

    """
    sensor_msg_thread: sends the periodic message broadcasting sensor information
    TODO: Replace with standardized class as all sensors need to do this
    """
    def sensor_msg_thread(self):
        while not self.end_f:
            message = {"data_addr": "localhost", "data_port": self.server_port}
            self.send_message(json.dumps(message).encode("utf-8"))
            time.sleep(1)

    def run(self):
        self.my_server.start()
        self.camera.start()
        self.sensor_msg_t.start()
        super().run()

    def recv_command(self, command: bytes):
        # used to receive a command
        command_i = struct.unpack("!B", command)
        print("Received Camera Command", command_i)
        self.camera.execute_command(command_i)