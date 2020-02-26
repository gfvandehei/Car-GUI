from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QAction
from lib.app.gui.apps.appscreen import AppScreen

class ScreenController(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CarGUI")
        self.menu = self.menuBar()
        self.toolbar = QToolBar("Actions")
        self._create_menu()
        self._create_toolbar()
        
        self.screen_stack = []
        self.change_screen(AppScreen(parent=self))
        self.show()
    
    def _create_menu(self):
        menubar = self.menuBar()
        menu = menubar.addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def _create_toolbar(self):
        self.addToolBar(self.toolbar)
        button_action = QAction("Back", self)
        button_action.setStatusTip("Go to the previous screen")
        button_action.triggered.connect(lambda: self.go_back_screen())
        self.toolbar.addAction(button_action)
    
    def change_screen(self, new_widget: QWidget):
        print(type(new_widget))
        self.screen_stack.append(type(new_widget))
        if(self.centralWidget()):
            self.centralWidget().close()
        self.setCentralWidget(new_widget)
        new_widget.show()
        print("SHOWED")
    
    def go_back_screen(self):
        if len(self.screen_stack) > 1:
            self.screen_stack.pop()
            back_screen_class = self.screen_stack[-1]
            back_screen = back_screen_class(parent=self)
            self.centralWidget().close()
            self.setCentralWidget(back_screen)
            back_screen.show()
        else:
            print("At base screen")
