import socket
from lib.app.sensors.sensor_factory import SensorFactory
from threading import Thread

class UDPDetector(Thread):
    
    def __init__(self, port: int):
        super().__init__()
        # Set up thread
        self.setName('UDPDetector')
        self.run_f = False

        # set up socket
        self.listening_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listening_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST, 1)
        self.listening_socket.settimeout(1)
        self.listening_socket.bind(("", port))

    def run(self):
        self.run_f = True
        while self.run_f:
            try:
                data, address = self.listening_socket.recvfrom(16000)
                #print("Received message from {}", address)
                SensorFactory.post_sensor_update(data)
            except socket.timeout:
                continue

    def close(self):
        self.run_f = False
        try:
            print("Waiting for thread {} to join".format(self.getName()))
            self.join(5)
            if self.isAlive():
                raise(Exception("thread {} did not join in 5 seconds".format(self.getName())))
            print("joined")
            self.listening_socket.close()
        except Exception:
            print("Forcing socket closed")
            self.listening_socket.close()

