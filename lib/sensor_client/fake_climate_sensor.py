import socket
from threading import Thread
import struct
import random
import time
import sys
class FakeClimateDetector(Thread):

    def __init__(self, mid=1, time_interval: int=1, host_port: int=8080):
        super().__init__()
        self.my_id = mid
        self.interval = time_interval
        self.host_port = host_port

        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockfd.bind(("", 0))

    def run(self):
        try:
            while True:
                temp_f = random.randint(70, 100)
                humidity_f = random.randint(10, 40)
                data = struct.pack("!IHff", self.my_id, 1, temp_f, humidity_f)
                print("Sending:", struct.unpack("!IHff", data))
                self.sockfd.sendto(data, ('<broadcast>', self.host_port)) 
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.sockfd.close()
            exit(0)

ida = int(sys.argv[1])
FakeClimateDetector(mid=ida).start()
