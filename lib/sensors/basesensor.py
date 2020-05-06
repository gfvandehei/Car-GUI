from threading import Thread
from queue import Queue
import struct
import socket

class BaseSensor(Thread):

    def __init__(self, mid=1, sensor_type: int=0, host_port: int=8080):
        super().__init__()
        self.my_id = mid
        self.mytype = sensor_type
        self.host_port = host_port

        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockfd.bind(("", 0))
        
        self.send_message_queue = Queue()

    def send_message(self, rest: bytes):
        header = struct.pack("!IH", self.my_id, self.mytype)
        message = header + rest
        self.send_message_queue.put(message)

    def run(self):
        try:
            while True:
                message = self.send_message_queue.get()
                print("Message length", len(message))
                self.sockfd.sendto(message, ("<broadcast>", self.host_port))
        except KeyboardInterrupt:
            self.sockfd.close()
            exit(0)
