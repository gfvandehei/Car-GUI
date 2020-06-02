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

    def connect_client(self):
        conn, addr = self.tcp_server.accept()
        conn.setblocking(0)
        self.inputs.append(conn)
        self.outputs.append(conn)
        self.msg_queues[conn] = Queue(10)
        print("A new client {} has connected".format(addr))
    
    def disconnect_client(self, descriptor: socket.socket):
        try:
            self.inputs.remove(descriptor)
            self.outputs.remove(descriptor)
            del self.msg_queues[descriptor]
            descriptor.close()
            print("Client", descriptor, "disconnected")
        except Exception as err:
            print("There was an exception on client disconnect", err)

    def register_commandable(self, commandable: Commandable):
        self.on_command_callbacks.append(commandable)

    def handle_command(self, command: bytes):
        # parse command
        # send command on to each commandable
        for commandable in self.on_command_callbacks:
            commandable.recv_command(command)

    def on_message(self, descriptor: socket.socket):
        client_recv = descriptor.recv(1024)
        if len(client_recv) == 0:
            self.disconnect_client(descriptor)
            return

        self.handle_command(client_recv)

    def run(self):
        while not self.end_f:
            read, write, exept = select.select(self.inputs, self.outputs, self.inputs)

            for i in read:
                if i is self.tcp_server:
                    # there was a new connection
                    self.connect_client()
                else:
                    # a client sent a command:
                    try:
                        self.on_message(i)
                    except Exception as err:
                        print("Error on_message():", err)
                        continue

            for i in write:
                if i in self.inputs:
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
                print("Socket {} closed with exeption".format(i))
                del self.msg_queues[i]
                i.close()


    def send_image(self, image):
        img_len = len(image)
        message = struct.pack(">L",img_len) + image
        for i in self.msg_queues:
            #print("Here!")
            q: Queue = self.msg_queues[i]
            q.put(message)

