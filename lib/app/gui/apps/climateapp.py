from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from lib.app.sensors.sensor import Sensor
from lib.app.gui.widgets.tachiometer import Tacheometer
#from lib.app.gui.controllers.screencontroller import ScreenController
from lib.app.gui.widgets.climate_sensor import ClimateSensorDisplay
from lib.app.sensors.sensor_factory import SensorFactory
from lib.app.sensors.sensor_climate import ClimateSensor
import time

class ClimateApp(QWidget):
    def __init__(self, parent=None):
        print("Parent Climate: ", parent)
        super().__init__(parent=parent)
        self.climate_sensor_dict = {}
        self.running = True
        
        SensorFactory.await_sensor(1, self.set_climate_sensor)

        self.climate_sensor: ClimateSensor = None
        self.my_layout = QVBoxLayout()
        self.no_sensor_label = QLabel("No Sensor Data Available")
        self.my_layout.addWidget(self.no_sensor_label)
        #self.tachiometer = Tacheometer("MPH", max_val=100)
        self.climate_sensor_d = ClimateSensorDisplay("Climate 1")
        self.my_layout.addWidget(self.climate_sensor_d)
        self.setLayout(self.my_layout)
    
    def set_climate_sensor(self, sensor):
        self.climate_sensor: ClimateSensor = sensor
        self.climate_sensor.subscribe(self.on_climate_values)
        print(sensor)

    def on_climate_values(self, values):
        (temp, hum, ) = values
        print("on climate values")
        self.climate_sensor_d.on_values(temp, hum)


        