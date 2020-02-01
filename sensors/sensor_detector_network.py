import socket
import struct
from threading import Thread
from sensors.sensor_detector import SensorDetector
from sensors.sensor_network import NetworkSensor
from core.logger import Logger
import sys


class NetworkSensorDetector(SensorDetector):

    def __init__(self, logger: Logger, broadcast_port=65000):
        super().__init__()
        self.logger = logger
        self.end_f = False
        
        self.socket_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_fd.settimeout(1)
        self.socket_fd.bind(('', broadcast_port))

        run_thread = Thread(target=self.run)
        run_thread.start()

    def run(self):
        self.logger.print_initialization_message("NetworkSensorDetector")
    
        while not self.end_f:
            try:
                data, addr = self.socket_fd.recvfrom(15000)
            except socket.timeout:
                continue

            try:
                sense_id, sense_tcp, sense_type = self.verify_data(data)
                new_network_sensor = Ne
                self.fire_connect_event(sense_id, sense_tcp, sense_type, addr)
            except Exception as err:
                print(err)
                continue
    
    def verify_data(self, data):
        # sensor broadcast connection is in the form 
        # | 8 bytes addr | 8 byte tcp port | 1 byte sensor type
        if len(data) < struct.calcsize("!IIB"):
            self.logger.print_error_message(1, "Received Malformatted sensor UDP message")
        else:
            (sense_id, tcp_port, sense_type) = struct.unpack('!IIB', data)
            self.logger.print_debug_msg(5, "id: {} | port: {} | type: {}".format(sense_id, tcp_port, sense_type))
            return sense_id, tcp_port, sense_type


