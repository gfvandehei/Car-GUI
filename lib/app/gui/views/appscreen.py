
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QGridLayout, QPushButton
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QWidget
from lib.app.gui.controllers.appcontroller import AppController

class AppScreen(QWidget):

    def __init__(self, app_controller: AppController, parent=None):
        super().__init__(parent)
        self.app_controller = app_controller
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.buttons = []
        self.refresh_ui()

    def refresh_ui(self):
        button_names = self.app_controller.get_app_list()
        for name, clas in button_names:
            new_button = QPushButton(name)
            new_button.clicked.connect(lambda clas: self.open_sub_widget(clas))
            self.buttons.append(new_button)
            print("Adding button", name)
            self.grid_layout.addWidget(new_button, 0, 0)
        self.show()
    
    def open_sub_widget(self, new_widget):
        self.close()
        self.parent.setCentralWidget(new_widget)
