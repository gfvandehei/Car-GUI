
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QGridLayout, QPushButton
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QWidget
from lib.app.gui.apps.climateapp import ClimateApp
#from lib.app.gui.controllers.screencontroller import ScreenController

class AppScreen(QWidget):

    def __init__(self, parent=None):
        print("Parent: ", parent)
        super().__init__(parent=parent)
        self.myparent = parent
        self.screen_controller = parent
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.apps = {
            "Climate Sensors": ClimateApp
        }
        self.buttons = []
        self.load_buttons()
        

    def load_buttons(self):
        for i, name in enumerate(self.apps):
            new_button = QPushButton(name)
            new_button_f = lambda: self.screen_controller.change_screen(self.apps[name](parent=self.myparent)) 
            new_button.clicked.connect(new_button_f)
            self.grid_layout.addWidget(new_button, i, 0)
            self.buttons.append(new_button)