from dependency_injector import providers
from sensors.sensor_detector_manager import SensorDetectorManager
from core.logger import Logger


class SensorManager(object):

    def __init__(self, sensor_detector: SensorDetectorManager, logger: Logger,
                 sensor_factory: providers.DelegatedFactory):
        self.sensorDetectorManager = sensor_detector
        self.sensor_factory = sensor_factory
        self.logger = logger
        self.sensorDetectorManager.register_callback(self.on_new_sensor)
        self.sensors = {}  # map of uid to object

    def on_new_sensor(self, sensor_id: int, sensor_tcp_port: int, sensor_type: int, sensor_address: (str, int)):
        if self.sensors.get(sensor_id) is None:
            # create sensor
            new_sensor = self.sensor_factory(sensor_id, sensor_tcp_port, sensor_type, sensor_address)
            self.sensors[sensor_id] = new_sensor
        else:
            self.logger.print_debug_msg(5, "Received a request for an already existing sensor to be created")