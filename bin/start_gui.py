import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar

from lib.app.gui.controllers.screencontroller import ScreenController
from lib.app.sensors.sensors import Sensors
from lib.app.core.core import Core

if __name__ == "__main__":
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
    app = QApplication(sys.argv)
    screen_controller: ScreenController = ScreenController()
    sys.exit(app.exec_())