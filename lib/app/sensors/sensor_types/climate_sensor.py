from lib.app.sensors.sensor import Sensor
import json


class ClimateSensor(Sensor):

    def __init__(self, sensor_id: str):
        super(ClimateSensor, self).__init__(sensor_id)
        self._sensor_type = "Climate"
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        print("Created Climate Sensor")

    def parse_data(self, message: bytes):
        print("Parsing message ", message)
        try:
            message_dict = json.loads(message)
            self.temperature = message_dict['temp']
            self.humidity = message_dict["hum"]
            self.pressure = message_dict["bar"]
            self.add_data_point([self.temperature, self.humidity, self.pressure])
        except Exception as err:
            print(err)