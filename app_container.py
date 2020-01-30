from dependency_injector import containers, providers
from sensors.sensor_store import SensorStore
from sensors.sensor_detector_manager import SensorDetectorManager

class AppContainer(containers.DeclarativeContainer):

    config = providers.Configuration('config')

    sensor_data_storage = providers.Singleton(SensorStore)
    sensor_detector_manager = providers.Singleton(SensorDetectorManager, )
    #sensor_manager = providers.Singleton()
    app_container = providers.Singleton(TestItem)