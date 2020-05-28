from lib.common.commandable import Commandable
import socket
import select
from queue import Queue, Empty
from threading import Thread
import struct

class TCPImageServer(Thread):
    def __init__(self, port):
        super().__init__()
        self.server_port = port
        self.end_f = False
        self.tcp_server: socket.socket = None
        self.inputs = []
        self.outputs = []
        self.msg_queues = {}

        self.on_command_callbacks = []
        self.init_server()

    def init_server(self):
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_server.setblocking(0)
        self.tcp_server.bind(("", self.server_port))
        self.tcp_server.listen()
        self.inputs.append(self.tcp_server)

    def run(self):
        while not self.end_f:
            read, write, exept = select.select(self.inputs, self.outputs, self.inputs)

            for i in read:
                if i is self.tcp_server:
                    # there was a new connection
                    new_client, cli_addr = i.accept()
                    new_client.setblocking(0)
                    self.inputs.append(new_client)
                    self.outputs.append(new_client)
                    self.msg_queues[new_client] = Queue(10)
                    print("Client {} connected".format(cli_addr))
                else:
                    # a client sent a command:
                    client_message = i.recv(1024)
                    if client_message:
                        print("Recv:", client_message)
                    else:
                        self.inputs.remove(i)
                        self.outputs.remove(i)
                        i.close()
                        del self.msg_queues[i]

            for i in write:
                try:
                    next_msg = self.msg_queues[i].get_nowait()
                except Empty:
                    continue
                    #self.outputs.remove(i)
                else:
                    #print(next_msg)
                    i.send(next_msg)

            for i in exept:
                self.inputs.remove(i)
                if i in self.outputs:
                    self.outputs.remove(i)
                i.close()
                print("Socket {} closed with exeption".format(i))
                del self.msg_queues[i]


    def send_image(self, image):
        img_len = len(image)
        message = struct.pack(">L",img_len) + image
        for i in self.msg_queues:
            #print("Here!")
            q: Queue = self.msg_queues[i]
            q.put(message)

    def register_commandable(self, commandable: Commandable):
        self.on_command_callbacks.append(commandable)

    def handle_command(self, command):
        # parse command
        # send command on to each commandable
        for commandable in self.on_command_callbacks:
            commandable.send_command(command)