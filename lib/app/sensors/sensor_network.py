import socket
from lib.app.core.logger import Logger
from lib.app.sensors.sensor import Sensor
from threading import Thread


class NetworkSensor(Sensor):

    def __init__(self, sensor_id: int, sensor_tcp_port: int, sensor_type: int, address: (str, int), logger: Logger):
        super().__init__(sensor_id, sensor_type)
        self.sensor_address = (address[0], sensor_tcp_port)
        self.logger = logger
        self.connected_flag = False
        self.tcp_connection: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_thread = None

    def fully_initialize(self):
        self.tcp_connection.settimeout(5)
        try:
            self.logger.print_debug_msg(2, "Attempting connection to {}".format(self.sensor_address))
            err_f = self.tcp_connection.connect(self.sensor_address)
            self.logger.print_debug_msg(2, "Succesfull connected to {}".format(self.sensor_address))
            self.connected_flag = True
        except socket.error:
            self.logger.print_error_message(5, "TCP connection could not be made to {}".format(self.sensor_address))
        except Exception as err:
            print(err)

        self.recv_thread = Thread(target=self.read_thread)
        self.recv_thread.start()

    def read_thread(self):
        message = ""
        while self.connected_flag:
            try:
                data: str = str(self.tcp_connection.recv(15000))
                print(data)
                if len(data) == 0:
                    # disconnect
                    self.connected_flag = False
                for i in data:
                    if i == '\n':
                        self.on_network_message(message)
                        message = ""
                    else:
                        message += i
            except Exception as err:
                self.logger.print_error_message(1, err)
                message = ""

    def on_network_message(self, message: str):
        #  current protocol is numeric values delimited by ,
        values = []
        message_list = message.split(",")
        for i in message_list:
            values.append(int(i))
        self.add_data_point(values)
