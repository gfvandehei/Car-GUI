from sensors.sensors import Sensors
from core.core import Core

Core.config.override({
    "sensors": {
        "storage_file": "store.json",
        "detect_network": True,
        "detect_serial": False
    },
    "logging": {
        "name": "App",
        "level": 5
    }
})
Sensors.sensor_test()
