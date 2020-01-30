from sensors.sensor_detector_network import NetworkSensorDetector
from core.logger import Logger


class SensorDetectorManager(object):

    def __init__(self, network: bool, serial: bool, logger: Logger):
        self.detectors = []
        if network:
            self.detectors.append(NetworkSensorDetector(logger))
        if serial:
            pass

    def register_callback(self, callback: callable):
        # check if callback follows args format
        for detector in self.detectors:
            detector.register_connection_listener(callback)
