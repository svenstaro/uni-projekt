#! /usr/bin/env python2.7

import sys
from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from debugger import Debugger
from memoryviewer import *
import debugger_rc

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.debugger = None
        self.ui = uic.loadUi('gui.ui', self)

        self.ui.editor.setReadOnly(True)

        # nearly (all) connects are done via qtdesigner
        self.ui.editor.breakpointSet.connect(self.breakpointSet)
        self.ui.editor.breakpointRemoved.connect(self.breakpointRemoved)

    def updateDisplay(self):
        if self.debugger:
            for i in range(1, 15):
                getattr(self.ui, "reg_"+str(i)).setText(str(self.debugger.register[i]))
            self.ui.ram.setData(''.join(map(chr, self.debugger.ram)))
            self.ui.Z.setState(self.debugger.Z)
            self.ui.N.setState(self.debugger.N)
            self.ui.C.setState(self.debugger.C)
            self.ui.V.setState(self.debugger.V)
            self.ui.editor.setPcLine(self.debugger.getContentLine(self.debugger.pc))
        else:
            for i in range(1, 15):
                getattr(self.ui, "reg_"+str(i)).setText('0')
            self.ui.ram.setData('')
            self.ui.Z.setState(False)
            self.ui.N.setState(False)
            self.ui.C.setState(False)
            self.ui.V.setState(False)
            self.ui.editor.setPcLine(0)

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
        self.debugger = None
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
            if self.debugger.hasReachedEnd(): #TODO make it huebsch
                self.debugger.reset()
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
    import gc
    gc.set_debug(gc.DEBUG_COLLECTABLE | gc.DEBUG_INSTANCES | gc.DEBUG_COLLECTABLE)
    app = QApplication(sys.argv)
    MainWindow().show()
    sys.exit(app.exec_())
