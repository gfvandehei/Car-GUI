from lib.app.sensors.sensor import Sensor
import struct

class ClimateSensor(Sensor):

    def __init__(self, sid: int):
        super().__init__(sid)
        
    def receive_update(self, raw_data: bytes):
        """
        DATA FORMAT: Temperature(f)(float) | Humidity(bar)(float)  
        """
        temperature_f, humidity_b = struct.unpack("!HH", raw_data)
        self.add_data_point([temperature_f, humidity_b])