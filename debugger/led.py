from PyQt4 import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Led(QWidget):

    toggled = pyqtSignal(bool, name="Toggled event")

    def __init__(self, parent):
        super(Led, self).__init__(parent)

        self._state = False
        self.colorOn = QColor("#0f0")
        self.colorOff = QColor("#f00")
        self.setMinimumWidth(22)
        self.setMinimumHeight(22)

    @pyqtProperty(bool)
    def state(self):
        return self._state
    @state.setter
    def state(self, state):
        self._state = state
        self.toggled.emit(state)
        self.repaint()

    @pyqtProperty(QColor)
    def colorOn(self):
        return self._colorOn
    @colorOn.setter
    def colorOn(self, value):
        self._colorOn = value

    @pyqtProperty(QColor)
    def colorOff(self):
        return self._colorOff
    @colorOff.setter
    def colorOff(self, value):
        self._colorOff = value

    def mouseDoubleClickEvent(self, _):
        self.state = not self.state

    def paintEvent(self, ev):
        minSize = min(self.width(), self.height()) - 2
        size = QSize(minSize, minSize)
        center = QPointF(size.width()/2.0, size.height()/2.0)
        gradient = QRadialGradient(center, minSize / 2.0, QPointF(center.x(), size.height()/3.0))
        color = self.colorOn if self.state else self.colorOff
        gradient.setColorAt(0.0, color.light(250))
        gradient.setColorAt(0.5, color.light(130))
        gradient.setColorAt(1.0, color)

        borderGradient = QConicalGradient(center, -90)
        borderColor = QColor(self.palette().dark())

        borderGradient.setColorAt(0.2, borderColor)
        borderGradient.setColorAt(0.5, QColor(self.palette().light()))
        borderGradient.setColorAt(0.8, borderColor)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(gradient))
        penBrush = QBrush(borderGradient)
        penWidth = minSize/ 8.0
        painter.setPen(QPen(penBrush, penWidth))

        r = QRectF(penWidth / 2.0, penWidth / 2.0, size.width() - penWidth, size.height() - penWidth)
        painter.drawEllipse(r)
        painter.end()




