from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from numpy import interp
import numpy as np
import math
from lib.app.gui.widgets.climategraph import PlotCanvas

class ClimateSensorDisplay(QtWidgets.QWidget):
    """
    Custom Qt Widget to show a power bar and dial.
    Demonstrating compound and custom-drawn widget.
    """

    def __init__(self, sensor_name: str, *args, **kwargs):
        super(ClimateSensorDisplay, self).__init__(*args, **kwargs)

        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        self.hum_plot_vals = []
        self.temp_plot_vals = []
        self.skip = 20
        #top row
        self.sensor_label = QtWidgets.QLabel(sensor_name)
        layout.addWidget(self.sensor_label, 0, 0, 1, 4)

        #second row
        self.temp_image = QtWidgets.QLabel("ASD")
        pixmap = QtGui.QPixmap('./resources/temperature.png')
        self.temp_image.setScaledContents(True)
        self.temp_image.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.temp_image.setPixmap(pixmap)
        self.sensor_temperature = QtWidgets.QLCDNumber()
        layout.addWidget(self.temp_image, 1, 0)
        layout.addWidget(self.sensor_temperature, 1, 1)
        

        #3rd row
        self.hum_image = QtWidgets.QLabel("ASDf")
        pixmap_h = QtGui.QPixmap('./resources/humidity.png')
        self.hum_image.setPixmap(pixmap_h)
        self.hum_image.setScaledContents(True)
        self.hum_image.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.hum_image.setPixmap(pixmap_h)
        self.sensor_humidity = QtWidgets.QLCDNumber()
        self.sensor_humidity.setDecMode()
        layout.addWidget(self.hum_image, 2, 0)
        layout.addWidget(self.sensor_humidity, 2, 1,)

        self.graphwidget = PlotCanvas()
        layout.addWidget(self.graphwidget, 3, 0, 4, 4)


    def on_values(self, temp, hum):
        self.sensor_temperature.display(temp)
        self.sensor_humidity.display(hum)
        #self.sensor_temperature.setText(str(temp))
        #self.sensor_humidity.setText(str(hum))
        
        pen1 = pg.mkPen(color='r')
        pen2 = pg.mkPen(color='b')
        time_arr = range(60)
        self.temp_plot_vals.append(temp)
        self.hum_plot_vals.append(hum)
        self.graphwidget.plot(self.temp_plot_vals, self.hum_plot_vals)