from dependency_injector import providers
from sensors.sensor_detector_manager import SensorDetectorManager
from core.logger import Logger
from sensors.sensor import Sensor


class SensorManager(object):

    def __init__(self, sensor_detector: SensorDetectorManager, logger: Logger):
        self.sensorDetectorManager = sensor_detector
        self.logger = logger
        self.sensorDetectorManager.register_callback(self.on_new_sensor)
        self.sensors = {}  # map of uid to object

    def on_new_sensor(self, new_sensor: Sensor):  # sensor_id: int, sensor_tcp_port: int, sensor_type: int, sensor_address: (str, int)):
        if self.sensors.get(new_sensor.get_id()) is None:
            # create sensor
            self.sensors[new_sensor.get_id()] = new_sensor
            new_sensor.fully_initialize()
        else:
            self.logger.print_debug_msg(5, "Received a request for an already existing sensor to be created")