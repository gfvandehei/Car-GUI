from lib.sensor_client.network_sensor.network_sensor import NetworkSensorNode
from lib.app.core.core import Core

Core.config.override({
    "client": {
        "id": 1,
        "tcp_port": 6879,
        "type": 1,
        "broadcast_port": 65500
    },
    "logging": {
        "name": "Network_Sensor",
        "level": 5
    }
})
NetworkSensorNode.run_network_sensor()
