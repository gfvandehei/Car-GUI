from lib.sensor_client.network_sensor.broadcaster import Broadcaster
import socket
from threading import Thread
from lib.sensor_client.network_sensor.datasource import DataSource
import select

class SessionManager(object):

    def __init__(self, broadcaster: Broadcaster, data_source: DataSource, tcp_port: int):
        self.broadcaster = broadcaster
        self.data_source = data_source
        self.data_source.subscribe(self.on_data_source)

        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.setblocking(0)
        self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_server.bind(("", tcp_port))

        bound_port = self.tcp_server.getsockname()[1]
        self.broadcaster.tcp_port = bound_port
        self.broadcaster.start_broadcast()

        self.tcp_server.listen(5)
        self.inputs = [self.tcp_server]
        self.outputs = []

        Thread(target=self.select_loop).start()

    def select_loop(self):
        while self.inputs:
            read_fd, write_fd, exept_fd = select.select(self.inputs, self.outputs, self.inputs)

            for sock_fd in read_fd:
                if sock_fd == self.tcp_server:
                    # we need to accept
                    new_connection, address = self.tcp_server.accept()
                    print("Accepted connection from {}".format(address))
                    new_connection.setblocking(0)
                    self.inputs.append(new_connection)
                    self.broadcaster.stop_broadcast()
                else:
                    data = sock_fd.recv(15000)
                    if len(data) == 0:
                        # disconnected
                        print("Disconnected")
                        self.inputs.remove(sock_fd)
                        self.broadcaster.start_broadcast()

                    print("Received data {}".format(data))

    def on_data_source(self, data: list):
        print("On_data_source")
        for i in self.inputs:
            if i == self.tcp_server:
                continue
            message = ""
            counter = 0
            for dp in data:
                counter += 1
                message += str(dp) + ","
            print(message, counter)
            if counter > 0:
                message = message[0:-1]
                message += "\n"
                flag = i.send(bytes(message, 'utf-8'))
                print(flag)
