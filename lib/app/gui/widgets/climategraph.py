from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def plot(self, temp_data, hum_data):
        ax = self.figure.add_subplot(111)
        if(len(temp_data) > 60 or len(hum_data) > 60):
            #self.figure.cla()
            ax.cla()
            ax.plot(temp_data[-60:], 'r')
            ax.plot(hum_data[-60:], 'b')
        else:
            ax.plot(temp_data, 'r')
            ax.plot(hum_data, 'b')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()