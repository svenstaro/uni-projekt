import sys
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('felix.ui', self)

        self.ui.actionOpen.triggered.connect(self.openNewFile)

    @pyqtSlot()
    def openNewFile(self):
        filename = QtGui.QFileDialog.getOpenFileNameAndFilter(self, 'Open File', filter="Compiled/Debug Files (*.out.dbg *.s.out) (*.out.dbg *.out);;All Files (*)")[0]
        if filename != '':
            with open(str(filename).rsplit('.', 1)[0]) as content:
                self.ui.frame.setText(content.read())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
