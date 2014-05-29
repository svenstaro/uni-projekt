#! /usr/bin/env python2.7

import sys
from functools import partial
from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from debugger import Debugger, DummyCpu
from memoryviewer import *
import debugger_rc

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.debugger = Debugger(DummyCpu())
        self.ui = uic.loadUi('gui.ui', self)

        self.ui.editor.setReadOnly(True)

        # nearly (all) connects are done via qtdesigner
        self.ui.editor.breakpointSet.connect(self.breakpointSet)
        self.ui.editor.breakpointRemoved.connect(self.breakpointRemoved)

        #TODO register on registerlabels
        for i in ['Z', 'N', 'C', 'V']:
            getattr(self.ui, i).toggled.connect(partial(lambda flag, state: setattr(self.debugger, flag, state), i))

        self.updateDisplay()


    def updateDisplay(self):
        for i in range(1, 15+1):
            getattr(self.ui, "reg_"+str(i)).setText(QString("%1").arg(self.debugger.register[i], base=10, fieldWidth=10, fillChar=QChar('0')))
        self.ui.ram.setData(''.join(map(chr, self.debugger.ram)))
        self.ui.Z.state = self.debugger.Z
        self.ui.N.state = self.debugger.N
        self.ui.C.state = self.debugger.C
        self.ui.V.state = self.debugger.V
        self.ui.editor.setPcLine(self.debugger.getContentLine(self.debugger.pc))

    @pyqtSlot()
    def openNewFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', filter="Compiled/Debug Files (*.out.dbg *.s.out) (*.out.dbg *.out);;All Files (*)")
        if filename != '':
            self.debugger = Debugger.loadFromFile(str(filename), memorysize=1024*1024)
            self.ui.ram.setData(''.join(map(chr, self.debugger.ram)))
            self.ui.editor.setText(self.debugger.fileContent())
            self.ui.editor.resetMarker()
        self.updateDisplay()

    @pyqtSlot()
    def closeFile(self):
        self.debugger.cpu = Debugger(DummyCpu())
        self.ui.ram.setData('')
        self.ui.editor.setText('')
        self.ui.editor.resetMarker()
        self.updateDisplay()

    @pyqtSlot(int)
    def ramChanged(self, index):
        self.debugger.ram[index] = self.ui.ram.data()[index]

    @pyqtSlot()
    def run(self):
        if self.debugger:
            self.debugger.run()
            self.updateDisplay()

    @pyqtSlot()
    def reset(self):
        if self.debugger:
            self.debugger.reset()
            self.updateDisplay()

    @pyqtSlot()
    def stepOver(self):
        if self.debugger:
            self.debugger.stepOver()
            self.updateDisplay()

    @pyqtSlot()
    def stepInto(self):
        if self.debugger:
            self.debugger.step()
            self.updateDisplay()

    @pyqtSlot(int)
    def breakpointSet(self, line):
        if self.debugger:
            self.debugger.breakpoints.append(self.debugger.getRomAddr(line))

    @pyqtSlot(int)
    def breakpointRemoved(self, line):
        if self.debugger:
            self.debugger.breakpoints.remove(self.debugger.getRomAddr(line))

    def contextMenuEvent(self, QContextMenuEvent):
        #disable rightclick menu
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow().show()
    sys.exit(app.exec_())
