from lib.app.sensors.sensor import Sensor
import socket
import json
from threading import Thread
import base64
import cv2
import struct
import numpy as np
import pickle

class CameraSensor(Sensor):

    def __init__(self, sensor_id: str):
        super().__init__(sensor_id)
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.data_transfer_addr = None
        self.img_cv2 = None

    def get_current_image(self):
        return self.img_cv2

    def pause(self):
        command = struct.pack("!B", 1)
        self.data_socket.send(command)

    def play(self):
        command = struct.pack("!B", 2)
        self.data_socket.send(command)

    def connect_tcp(self):
        try:
            self.data_socket.connect(self.data_transfer_addr)
            print("Connected")
            Thread(target=self.recv_image_thread).start()
        except Exception as err:
            self.data_transfer_addr = None
            print(err)

    def append_image_bytes(self, image_bytes: bytes):
        frame = base64.b64decode(image_bytes)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #print(frame.shape[0], frame.shape[1])
        print("IMAGE")
        self.img_cv2 = frame
        #print(len(base_64_decode))
        #cv2.imshow("image", frame)

    def recv_image_thread(self):
        data_msg = b''
        while True:
            data = self.data_socket.recv(4096)
            index = data.find(b'\n')
            if index > -1:
                while index != -1:
                    data_msg = data_msg+data[:index]
                    self.append_image_bytes(data_msg)
                    if index != len(data):
                        data = data[index+1:]
                    else: 
                        data = b''
                    data_msg = b''
                    index = data.find(b'\n')
            else:
                data_msg = data

    def parse_data(self, message: bytes):
        print("Parsing message ", message)
        try:
            message_dict = json.loads(message.decode('utf-8'))
            temp_addr = (message_dict['data_addr'], message_dict['data_port'])
            if self.data_transfer_addr != temp_addr:
                self.data_transfer_addr = temp_addr
                self.connect_tcp()
            #self.add_data_point([self.temperature, self.humidity, self.pressure])
        except Exception as err:
            print(err)