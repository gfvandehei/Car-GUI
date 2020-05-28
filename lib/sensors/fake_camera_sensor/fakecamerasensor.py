from lib.sensors.basesensor import BaseSensor
import socket
import cv2
import base64
import numpy as np
import time
from threading import Thread
import json
import select
import pickle
import struct 
class FakeCameraSensor(BaseSensor):

    def __init__(self, image_file: str, port: int, *args):
        super().__init__(*args)
        self.mytype = 2
        self.end_f = False
        self.server_port = port
        
        image = cv2.imread(image_file)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        retval, buffer = cv2.imencode('.jpg', image, encode_param)
        self.img_as_text = pickle.dumps(buffer, 0)
        self.img_size = len(self.img_as_text)
        # start server
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_server.bind(("", port))
        self.tcp_server.listen()

        self.clients = [self.tcp_server]

        self.server_t = Thread(target=self.server_thread)
        self.pic_t = Thread(target=self.get_pic_thread)
        self.sensor_msg_t = Thread(target=self.sensor_msg_thread)
    
    def get_pic_thread(self):
        while not self.end_f:
            for i in self.clients:
                if i == self.tcp_server:
                    continue
                i.sendall(struct.pack(">L",self.img_size) + self.img_as_text)
                print("sent")

            # 60 fps
            time.sleep(1/60)

    def server_thread(self):
        while not self.end_f:
            recv, write, exep = select.select(self.clients, [], [])

            for fd in recv:
                if fd == self.tcp_server:
                    new_client, addr = self.tcp_server.accept()
                    self.clients.append(new_client)
                else:
                    msg = fd.recv(1024)
                    print("Error: recieved", msg, "Should not recv anything on TCP")
            
    def sensor_msg_thread(self):
        while not self.end_f:
            #for i in self.split_image():
                #self.send_message(i)
            #time.sleep(1/60)
            message = {"data_addr": "localhost", "data_port": self.server_port}
            self.send_message(json.dumps(message).encode("utf-8"))
            time.sleep(1)

    def run(self):
        self.server_t.start()
        self.pic_t.start()
        self.sensor_msg_t.start()
        super().run()



