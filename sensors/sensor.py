import socket
from core.logger import Logger


class Sensor(object):
    def __init__(self, sensor_id: int, sensor_tcp_port: int, sensor_type: int, address: (str, int), logger: Logger):
        self.sid = sensor_id
        self.sensor_type = sensor_type
        self.sensor_address = (address[0], sensor_tcp_port)
        self.logger = logger
        self.connected_flag = False
        logger.print_initialization_message("New Sensor")

        self.tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_connection.settimeout(5)
        try:
            logger.print_debug_msg(2, "Attempting connection to {}".format(self.sensor_address))
            self.sensor_tcp_socket = self.tcp_connection.connect(self.sensor_address)
            logger.print_debug_msg(2, "Succesfull connected to {}".format(self.sensor_address))
            self.connected_flag = True
        except socket.error:
            logger.print_error_message(5, "TCP connection could not be made to {}".format(self.sensor_address))
        except Exception as err:
            print(err)