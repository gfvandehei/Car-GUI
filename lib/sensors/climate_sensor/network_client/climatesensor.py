from threading import Thread
import socket
import serial
import random
import struct

class ClimateSensor(Thread):

    def __init__(self, mid=1, time_interval: int=1, host_port: int=8080, serial_port: str="/dev/ACMtty0"):
        super().__init__()
        self.my_id = mid
        self.interval = time_interval
        self.host_port = host_port

        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockfd.bind(("", 0))

        self.serial = serial.Serial(serial_port, 56100)

    def run(self):
        try:
            while True:
                data_serial = str(self.serial.read_until("\n"))
                data_split = data_serial.split(",")
                #temp_f = random.randint(70, 100)
                #humidity_f = random.randint(10, 40)
                data = struct.pack("!IHff", self.my_id, 1, float(data_split[0]), float(data_split[1]))
                print("Sending:", struct.unpack("!IHff", data))
                self.sockfd.sendto(data, ('<broadcast>', self.host_port)) 
        except KeyboardInterrupt:
            self.sockfd.close()
            exit(0)
