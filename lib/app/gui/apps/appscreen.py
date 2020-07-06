
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QGridLayout, QPushButton
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QWidget
from lib.app.gui.apps.climateapp import ClimateApp
from lib.app.gui.apps.singlecameraapp import SingleCameraApp
#from lib.app.gui.controllers.screencontroller import ScreenController

class AppScreen(QWidget):

    def __init__(self, navigate):
        super().__init__()
       
        self.navigate: callable = navigate
        print(navigate)

        grid_layout = QGridLayout(self)

        climateButton = QPushButton(self)
        climateButton.clicked.connect(lambda: self.navigate(1))
        rearCamera = QPushButton(self)
        rearCamera.clicked.connect(lambda: self.navigate(2))

        grid_layout.addWidget(climateButton, 0, 0)
        grid_layout.addWidget(rearCamera, 0, 1)

        self.setLayout(grid_layout)

    