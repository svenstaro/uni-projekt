#! /usr/bin/env python2.7

import sys
from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from debugger import Debugger
from asmeditor import AsmEditor
import debugger_rc

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.debugger = None

        self.ui = uic.loadUi('gui.ui', self)

        self.ui.actionOpen.triggered.connect(self.openNewFile)

    @pyqtSlot()
    def openNewFile(self):
        filename = QtGui.QFileDialog.getOpenFileNameAndFilter(self, 'Open File', filter="Compiled/Debug Files (*.out.dbg *.s.out) (*.out.dbg *.out);;All Files (*)")[0]
        if filename != '':
            self.debugger = Debugger.loadFromFile(filename)
            with open(str(filename).rsplit('.', 1)[0]) as content:
                self.ui.textEdit.setText(content.read())

    @pyqtSlot()
    def cont(self):
        if self.debugger:
            self.debugger.run()

    @pyqtSlot()
    def stepOver(self):
        if self.debugger:
            self.debugger.stepOver()

    @pyqtSlot()
    def stepInto(self):
        if self.debugger:
            self.debugger.step()

    @pyqtSlot()
    def stepOut(self):
        if self.debugger:
            self.debugger.stepOut()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
