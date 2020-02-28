from lib.app.sensors.sensor import Sensor
from lib.app.sensors.sensor_datapipe_base import SensorDatapipe
import json


class ClimateSensor(Sensor):

    def __init__(self, sensor_id: str, sensor_datapipe: SensorDatapipe):
        super(ClimateSensor, self).__init__(sensor_id)
        self.sensor_datapipe: SensorDa = sensor_datapipe
        self._sensor_type = "Climate"
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

        self.sensor_datapipe.register_ondata_callback(self.parse_data)

    def parse_data(self, message: bytes):
        try:
            message_dict = json.loads(message)
            self.temperature = message_dict['temp']
            self.humidity = message_dict["hum"]
            self.pressure = message_dict["bar"]
            self.add_data_point([self.temperature, self.humidity, self.pressure])
        except Exception as err:
            print(err)