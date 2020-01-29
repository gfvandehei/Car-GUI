from dependency_injector import containers, providers

class SensorManager(object):

    def __init__(self, sensor_storage=None, logger=None):
        self.sensor_store = sensor_storage
        self.logger = logger

        self.SensorSensor
