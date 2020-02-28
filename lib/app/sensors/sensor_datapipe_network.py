from lib.app.sensors.sensor_datapipe_base import SensorDatapipe
from enum import Enum
import socket
import time


class SensorDatapipeNetwork(SensorDatapipe):

    def __init__(self, address: str, port: int):
        super().__init__()
        self.address = (address, port)
        self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sd.settimeout(1)
        self._connect(address, port)

    def _connect(self, address, port):
        self.state = SensorDatapipeNetworkStates.CONNECTING
        self.fire_onstate(state)
        try:
            self.sd.connect((address, port))
            self.change_state(SensorDatapipeNetworkStates.CONNECTED)
            return True
        except Exception as err:
            self.change_state(SensorDatapipeNetworkStates.ERROR)
        return False
    
    def _reconnect_loop(self):
        while not self.close and self.state == SensorDatapipeNetworkStates.CONNECTING:
            if(self._connect(self.address[0], self.address[1])):
                self._receive()
            time.sleep(1)

    def _receive(self):
        message_frag = b''
        while self.state == SensorDatapipeNetworkStates.CONNECTED:
            try:
                data = self.sd.recv(15000, 0)

                if len(data) == 0:
                    # disconnected
                    self.change_state(SensorDatapipeNetworkStates.CONNECTING)
                else:
                    #self.fire_ondata(data)
                    index = data.find('\r\n')
                    while index != -1:
                        message = message_frag+data[0:index]
                        self.fire_ondata(message)
                        message_frag = b''
                        data = data[index:]
                        index = data.find('\r\n')
                    message_frag = data



            except socket.timeout:
                continue
            except Exception as err:
                print(err)
        if self.close:
            return



class SensorDatapipeNetworkStates(Enum):
    INITIALIZING = 0
    CONNECTING = 1
    CONNECTED = 2
    ERROR = 4
