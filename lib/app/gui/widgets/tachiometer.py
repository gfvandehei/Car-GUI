from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class _Tach(QtWidgets.QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_angle = 240*16

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self.value = 0

    def sizeHint(self):
        return QtCore.QSize(40, 120)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(Qt.green, 10, Qt.SolidLine))
        painter.setBrush(QtCore.Qt.white)
        painter.drawArc(40, 40, 400, 400, self.start_angle,  self.value*-16)

        painter.end()

    def _trigger_refresh(self, value: int):
        self.value = value % 256
        print(self.value)
        self.update()


class Tacheometer(QtWidgets.QWidget):
    """
    Custom Qt Widget to show a power bar and dial.
    Demonstrating compound and custom-drawn widget.
    """

    def __init__(self, steps=5, *args, **kwargs):
        super(Tacheometer, self).__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout()
        self._tach = _Tach()
        layout.addWidget(self._tach)

        self._dial = QtWidgets.QDial()
        layout.addWidget(self._dial)
        self._dial.valueChanged.connect(
            self._tach._trigger_refresh
        )

        self.setLayout(layout)