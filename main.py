import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from QTCarGUI.iconmanager import IconManager

class Main(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.icon_manager = IconManager(self)
        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('PyCarGUI')
        self.setWindowIcon(QIcon('web.png'))
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())