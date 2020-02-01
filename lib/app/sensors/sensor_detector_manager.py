from lib.app.sensors.sensor_detector_network import NetworkSensorDetector
from lib.app.core.logger import Logger


class SensorDetectorManager(object):

    def __init__(self, network: NetworkSensorDetector, logger: Logger):
        self.detectors = []
        self.logger = logger
        self.detectors.append(network)

    def register_callback(self, callback: callable):
        # check if callback follows args format
        for detector in self.detectors:
            detector.register_connection_listener(callback)
