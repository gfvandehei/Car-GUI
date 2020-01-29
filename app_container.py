from dependency_injector import containers, providers
from sensors.sensor_store import SensorStore

class AppContainer(containers.DeclarativeContainer):

    config = providers.Configuration('config')

    sensor_data_storage = providers.Singleton(SensorStore)
    sensor_manager = providers.Singleton()