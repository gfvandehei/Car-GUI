from dependency_injector import containers, providers
from lib.sensor_client.network_sensor.broadcaster import Broadcaster
from lib.app.core.core import Core


def main(broadcaster):
    pass


class NetworkSensorNode(containers.DeclarativeContainer):

    broadcaster = providers.Singleton(Broadcaster,
                                      sense_id=Core.config.client.id,
                                      tcp_port=Core.config.client.tcp_port,
                                      sense_type=Core.config.client.type,
                                      broadcast_port=Core.config.client.broadcast_port,
                                      logger=Core.logger)

    run_network_sensor = providers.Callable(main, broadcaster=broadcaster)

