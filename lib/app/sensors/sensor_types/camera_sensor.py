from lib.app.sensors.sensor import Sensor
import socket
import json
from threading import Thread
import base64

class CameraSensor(Sensor):

    def __init__(self):
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.data_transfer_addr = None
        self.img_bytes = b''

    def connect_tcp(self):
        try:
            self.data_socket.connect(self.data_transfer_addr)
            Thread(target=self.recv_image_thread).start()
        except Exception as err:
            self.data_transfer_addr = None
            print(err)

    def append_image_bytes(self, image_bytes: bytes):
        base_64_raw = image_bytes.decode('utf-8')
        base_64_decode = base64.b64decode(base_64_raw)
        print(base_64_decode)

    def recv_image_thread(self):
        data_msg = b''
        while True:
            data = self.data_socket.recv(1024)
            if len(data) == 0:
                # disconnected
                return

            index = data.find("\n")
            while index > 0:
                data_msg += data[:index]
                # data_msg contains image bytes
                if index != len(data)-1:
                    data = data[index+1:]
                index = data.find("\n")
                self.append_image_bytes(data_msg)

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