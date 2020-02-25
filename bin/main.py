from lib.app.sensors.sensors import Sensors
from lib.app.core.core import Core
from lib.app.gui.gui import AppGUI

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
#print(Core.config.get_name('logging'))
#Sensors.sensor_manager()
#Sensors.sensor_test()
AppGUI().run()