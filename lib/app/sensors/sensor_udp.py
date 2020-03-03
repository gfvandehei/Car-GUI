from lib.common.singleton import Singleton
from lib.app.sensors.sensor_manager import SensorManager
from threading import Thread
import socket 


@Singleton
class SensorUDPCollector(object):

    def __init__(self, port):
        self.sensor_manager = SensorManager.Instance()
        self.end_f = False

        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockfd.settimeout(1)
        self.sockfd.bind(('', port))

        self.recv_thread = Thread(target=self.recv_messages)
        self.recv_thread.start()

    def recv_messages(self):
        while not self.end_f:
            try:
                data, addr = self.sockfd.recvfrom(15000)
                
            except socket.timeout:
                continue

