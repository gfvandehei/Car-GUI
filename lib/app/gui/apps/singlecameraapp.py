from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from lib.app.sensors.sensor import Sensor
from lib.app.gui.widgets.tachiometer import Tacheometer
#from lib.app.gui.controllers.screencontroller import ScreenController
from lib.app.gui.widgets.climate_sensor import ClimateSensorDisplay
from lib.app.sensors.sensor_factory import SensorFactory
from lib.app.sensors.sensor_types.camera_sensor import CameraSensor
import time
from threading import Thread

"""class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, parent, camera: CameraSensor):
        super().__init__(parent)
        self.camera: CameraSensor = camera

    def run(self):
        while True:
            frame = self.camera.get_current_image()
            if frame is not None:
                # https://stackoverflow.com/a/55468544/6622587
                h, w, ch = frame.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)"""

class SingleCameraApp(QWidget):
    def __init__(self, parent=None):
        print("Parent Climate: ", parent)
        super().__init__(parent=parent)
        self.camera_sensor_dict = {}
        self.running = True

        self.my_layout = QHBoxLayout()
        self.setLayout(self.my_layout)
        self.th = None
        self.label = QLabel(self)
        self.label.resize(640, 480)

        SensorFactory.await_sensor(1, self.camera_connect)
        #SensorFactory.await_sensor(2, self.set_climate_sensor_exterior)

    def camera_connect(self, camera: CameraSensor):
        self.th = Thread(target=self.getImageThread, args=(camera,))
        self.th.start()

    def getImageThread(self, camera):
        while True:
            frame = camera.get_current_image()
            if frame is not None:
                h, w, ch = frame.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.label.setPixmap(QPixmap.fromImage(p))

    """def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))"""




        