import socket
import time
import struct
from threading import Thread
from lib.app.core.logger import Logger


class Broadcaster(object):

    def __init__(self, sense_id: int, tcp_port: int, sense_type: int, broadcast_port: int, logger: Logger):
        self.logger = logger
        self.sense_id = sense_id
        self.tcp_port = tcp_port
        self.sense_type = sense_type
        self.broadcast_port = broadcast_port
        self.active_broadcast = False

        self.broadcaster_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcaster_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcaster_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcaster_socket.bind(('', broadcast_port))

        self.message = None 
        self.broadcast_thread = None
        # self.start_broadcast()

    def start_broadcast(self):
        self.logger.print_debug_msg(5, "Broadcast is starting")
        self.message = struct.pack('!IIB', self.sense_id, self.tcp_port, self.sense_type)
        if self.broadcast_thread:
            return
        self.active_broadcast = True
        self.broadcast_thread = Thread(target=self.broadcast)
        self.broadcast_thread.start()

    def broadcast(self):
        while self.active_broadcast:
            self.broadcaster_socket.sendto(self.message, ('', self.broadcast_port))
            time.sleep(5)

    def stop_broadcast(self):
        self.logger.print_debug_msg(5, "Broadcast is stopping")
        self.active_broadcast = False
        if self.broadcast_thread:
            self.broadcast_thread.join()
