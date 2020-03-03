import struct

class SensorUDPMessageFactory(object):

    @staticmethod
    def contruct_udp_message(databytes: bytes) -> BaseSensorMessage:
        sid, stype = struct.unpack("!II", databytes[0:8])

class BaseSensorMessage(object):
    def __init__(self, sender_id):
        self.sender_id = sender_id

    @property
    def get_id(self):
        return self.sender_id

class ClimateSensorMessage(BaseSensorMessage):
    def __init__(self, sender_id, temperature_f, humidity_per, pressure_bar):
        super().__init__(sender_id)
        self.temp = temperature_f
        self.humidity = humidity_per
        self.pressure = pressure_bar

    @classmethod
    def create_climate_message(cls, recv_bytes: bytes) -> ClimateSensorMessage:
        sid, stype, temp, humi, bar = struct.unpack("!IIhhh", recv_bytes)
        return ClimateSensorMessage(sid, temp, humi, bar)

class ImageSensorMessage(BaseSensorMessage):
    def __init__(self, sender_id, imagex, imagey, imagebytes):
        super().__init__(sender_id)
        self.image_size = (imagex, imagey)
        self.image = imagebytes

    @classmethod
    def create_image_message(cls, recv_bytes: bytes) -> ImageSensorMessage:
        sid, stype, imagex, imagey, image = struct.unpack("!IIhh{}s")

