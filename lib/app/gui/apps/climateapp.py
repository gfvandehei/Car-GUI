from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from lib.app.sensors.sensors import Sensors
from lib.app.sensors.sensor_manager import SensorManager
from lib.app.sensors.sensor import Sensor
from lib.app.gui.widgets.tachiometer import Tacheometer
#from lib.app.gui.controllers.screencontroller import ScreenController

class ClimateApp(QWidget):
    def __init__(self, parent=None):
        print("Parent Climate: ", parent)
        super().__init__(parent=parent)
        self.sensor_manager: SensorManager = Sensors.sensor_manager()
        self.climate_sensor_dict = {}

        self.my_layout = QVBoxLayout()
        self.no_sensor_label = QLabel("No Sensor Data Available")
        self.my_layout.addWidget(self.no_sensor_label)
        self.tachiometer = Tacheometer()
        self.my_layout.addWidget(self.tachiometer)
        self.setLayout(self.my_layout)

        self.show_climate_sensors()
        

    def show_climate_sensors(self):
        if len(self.sensor_manager.sensors) == 0:
            print("There are no sensors/climate sensors to show")
            self.no_sensor_label.show()
        else:
            self.no_sensor_label.hide()
            for i in self.sensor_manager.sensors:
                new_sensor_widget = QLabel(i.get_id())
                self.my_layout.addWidget(new_sensor_widget)

        