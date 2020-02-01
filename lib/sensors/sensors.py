from dependency_injector import containers, providers
from lib.sensors.sensor_manager import SensorManager
from lib.sensors.sensor_store import SensorStore
from lib.sensors.sensor_detector_manager import SensorDetectorManager
from lib.sensors.sensor_network import Sensor
from lib.sensors.sensor_network import NetworkSensor
from lib.core.core import Core
from lib.sensors.sensor_detector_network import NetworkSensorDetector

def main(s, s1, s2):
    return


class Sensors(containers.DeclarativeContainer):

    sensor_storage = providers.Singleton(SensorStore,
                                         logger=Core.logger,
                                         sensor_io_file=Core.config.sensors.storage_file)


    # different sensor type factories
    network_sensor_factory = providers.DelegatedFactory(NetworkSensor,
                                                        logger=Core.logger)

    # sensor_managers
    network_sensor_manager = providers.Singleton(NetworkSensorDetector,
                                                 network_sensor_factory=network_sensor_factory,
                                                 broadcast_port=Core.config.sensors.network.port,
                                                 logger=Core.logger)

    sensor_detector_manager = providers.Singleton(SensorDetectorManager,
                                                  network=network_sensor_manager,
                                                  logger=Core.logger)

    sensor_manager = providers.Singleton(SensorManager,
                                         sensor_detector=sensor_detector_manager,
                                         logger=Core.logger)

    sensor_test = providers.Callable(main, s=sensor_storage, s1=sensor_detector_manager, s2=sensor_manager)


