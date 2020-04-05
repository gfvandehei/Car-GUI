
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QWidget

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('CarGUI')
        self._createMenu()
        self.setMainWidget(QLabel("asdasd"))

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)
    
    def setMainWidget(self, passed: QWidget):
        print(self.centralWidget())
        if self.centralWidget() is not None:  # then we need to deinit
            central: QWidget = self.centralWidget()
            central.close()
        self.setCentralWidget(passed)