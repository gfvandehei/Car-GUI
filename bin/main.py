from lib.app.sensors.sensors import Sensors
from lib.app.core.core import Core

Core.config.override({
    "sensors": {
        "storage_file": "store.json",
        "network": {
            "port": 65500
        }
    },
    "logging": {
        "name": "App",
        "level": 5
    }
})
Sensors.sensor_test()
