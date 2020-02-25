"""from lib.app.gui.initscreen import MainScreen
import kivy
kivy.require('1.0.6')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


class RootWidget(Screen):
    pass


Builder.load_file(dir_path+"/kv/root.kv")


class AppGUI(App):
    def __init__(self, **kwargs):
        super(AppGUI, self).__init__(**kwargs)
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(RootWidget(name="root"))
        self.screen_manager.add_widget(MainScreen(name="main_screen"))

    def build(self):
        return self.screen_manager"""


import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from lib.app.gui.views.mainwindow import MainWindow
from lib.app.gui.controllers.appcontroller import AppController
from lib.app.gui.guicontainer import GUIContainer

if __name__ == "__main__":
    GUIContainer.config.override({
        "apppath": "./lib/app/gui/apps"
    })

    app = QApplication(sys.argv)
    AppController()
    win = MainWindow()
    win.setMainWidget(GUIContainer.app_screen(parent=win))
    win.show()
    sys.exit(app.exec_())