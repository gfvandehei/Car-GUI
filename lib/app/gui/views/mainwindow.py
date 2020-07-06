
import sys

"""from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QStackedWidget"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import*

from lib.app.gui.apps.appscreen import AppScreen
from lib.app.gui.apps.climateapp import ClimateApp

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('CarGUI')

        # Initialize all the pages
 

        # initialize the pages into the stack
        self.stack = QStackedWidget(self)

        self.app_page = AppScreen(self.stack.setCurrentIndex)
        self.climate_page = ClimateApp()

        self.stack.addWidget(self.app_page)
        self.stack.addWidget(self.climate_page)
        #initialize most of the main window
        self.setCentralWidget(self.stack)
        self.setWindowTitle("OpenDash")
        self.resize(1920, 1080)
        self._createMenu()
        self.show()
        
    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)