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

    def connect_tcp(self):
        try:
            self.data_socket.connect(self.data_transfer_addr)
            print("Connected")
            Thread(target=self.recv_image_thread).start()
        except Exception as err:
            self.data_transfer_addr = None
            print(err)

    def append_image_bytes(self, image_bytes: bytes):
        frame = pickle.loads(image_bytes, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #print(frame.shape[0], frame.shape[1])
        print("IMAGE")
        self.img_cv2 = frame
        #print(len(base_64_decode))
        #cv2.imshow("image", frame)

    def recv_image_thread(self):
        data_msg = b''
        payload_size = struct.calcsize(">L")
        while True:
            while len(data_msg) < payload_size:
                #print("Recv: {}".format(len(data_msg)))
                data_msg = self.data_socket.recv(4096)
                #print(data_msg)
            
            packed_msg_size = data_msg[:payload_size]
            data_msg = data_msg[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            #print(msg_size)
            #print("msg_size: {}".format(msg_size))
            while len(data_msg) < msg_size:
                data_msg += self.data_socket.recv(4096)
            frame_data = data_msg[:msg_size]
            data_msg = data_msg[msg_size:]
            self.append_image_bytes(frame_data)

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