from dependency_injector import containers, providers
from sensors.sensor_manager import SensorManager
from sensors.sensor_store import SensorStore
from sensors.sensor_detector_manager import SensorDetectorManager
from sensors.sensor import Sensor
from core.core import Core


def main(s, s1, s2):
    return


class Sensors(containers.DeclarativeContainer):

    sensor_storage = providers.Singleton(SensorStore,
                                         logger=Core.logger,
                                         sensor_io_file=Core.config.sensors.storage_file)

    sensor_detector_manager = providers.Singleton(SensorDetectorManager,
                                                  network=Core.config.sensors.detect_network,
                                                  serial=Core.config.sensors.detect_serial,
                                                  logger=Core.logger)

    sensor_factory = providers.DelegatedFactory(Sensor,
                                                logger=Core.logger)

    sensor_manager = providers.Singleton(SensorManager,
                                         sensor_factory=sensor_factory,
                                         sensor_detector=sensor_detector_manager,
                                         logger=Core.logger)

    sensor_test = providers.Callable(main, s=sensor_storage, s1=sensor_detector_manager, s2=sensor_manager)


