from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class AppScreenButton(QtWidgets.QPushButton):
    """description of class"""

    def __init__(self, *args):
        super().__init__(*args)
        self.barcolor = QtGui.QColor(255, 0, 0, 255)
        self.text = "Not set"
        self.setMinimumSize(375,375)
        self.setStyleSheet(
            """
            background-color: rgba(255,255,255, .1);
            border-radius: 100px;
            """
        )

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(255, 255, 255, 20))
        brush.setStyle(Qt.SolidPattern)

        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        brush.setColor(self.barcolor)
        rect = QtCore.QRect(0, 0, painter.device().width(), int(painter.device().height()/15))
        painter.fillRect(rect, brush)

        #rect = QtCore.QRect(0, painter.device().height()-painter.device().height()/10, painter.device().width(), painter.device().height())
        height = painter.device().height()
        rect = QtCore.QRect(0, 150, painter.device().width(), painter.device().height())
        painter.setFont(QtGui.QFont('Arial', 15))
        painter.drawText(rect, Qt.AlignCenter, self.text)

        painter.end()
