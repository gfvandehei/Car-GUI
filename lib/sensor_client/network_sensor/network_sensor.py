from dependency_injector import containers, providers
from lib.sensor_client.network_sensor.broadcaster import Broadcaster
from lib.app.core.core import Core
from lib.sensor_client.network_sensor.random_data_source import RandomDataSource
from lib.sensor_client.network_sensor.sessionmanager import SessionManager


def main(session_manager):
    pass


class NetworkSensorNode(containers.DeclarativeContainer):

    broadcaster = providers.Singleton(Broadcaster,
                                      sense_id=Core.config.client.id,
                                      tcp_port=Core.config.client.tcp_port,
                                      sense_type=Core.config.client.type,
                                      broadcast_port=Core.config.client.broadcast_port,
                                      logger=Core.logger)

    data_source = providers.Singleton(RandomDataSource)

    session_manager = providers.Singleton(SessionManager,
                                          broadcaster=broadcaster,
                                          data_source=data_source,
                                          tcp_port=Core.config.client.tcp_port)

    run_network_sensor = providers.Callable(main, session_manager=session_manager)

