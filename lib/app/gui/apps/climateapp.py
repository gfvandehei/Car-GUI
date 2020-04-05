from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
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
        
        self.climate_sensor_i: ClimateSensor = None
        self.climate_sensor_o: ClimateSensor = None
        self.my_layout = QHBoxLayout()
        self.setLayout(self.my_layout)

        self.no_sensor_label = QLabel("No Sensor Data Available")
        self.my_layout.addWidget(self.no_sensor_label)
        #self.tachiometer = Tacheometer("MPH", max_val=100)
        self.climate_sensor_d = ClimateSensorDisplay("Interior:")
        self.my_layout.addWidget(self.climate_sensor_d)
        self.climate_sensor_d.hide()
        

        self.climate_sensor_e = ClimateSensorDisplay("Exterior:")
        self.my_layout.addWidget(self.climate_sensor_e)
        self.climate_sensor_e.hide()
        
        SensorFactory.await_sensor(1, self.set_climate_sensor_interior)
        SensorFactory.await_sensor(2, self.set_climate_sensor_exterior)

    def set_climate_sensor_interior(self, sensor):
        self.no_sensor_label.hide()
        self.climate_sensor_d.show()
        self.climate_sensor_i: ClimateSensor = sensor
        self.climate_sensor_i.subscribe(self.on_climate_values_in)
        print(sensor)

    def set_climate_sensor_exterior(self, sensor):
        self.no_sensor_label.hide()
        self.climate_sensor_e.show()
        self.climate_sensor_o: ClimateSensor = sensor
        self.climate_sensor_o.subscribe(self.on_climate_values_out)
        print(sensor)

    def on_climate_values_in(self, values):
        (temp, hum, ) = values
        print("on climate values")
        self.climate_sensor_d.on_values(temp, hum)

    
    def on_climate_values_out(self, values):
        (temp, hum, ) = values
        print("on climate values")
        self.climate_sensor_e.on_values(temp, hum)


        