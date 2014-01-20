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
        self.decoder = AsmDecoder()
        self.ui = uic.loadUi('gui.ui', self)

        self.ui.editor.setReadOnly(True)
        self.ui.rom.setDecoder(self.decoder)
        self.ui.rom.setReadOnly(True)
        self.ui.rom.setOverwriteMode(False)
        self.ui.rom.setNoOfBytesPerLine(4)

        self.ui.editor.breakpointSet.connect(self.breakpointset)
        self.ui.editor.breakpointRemoved.connect(self.breakpointremoved)
        self.ui.ram.dataChanged.connect(self.ramChanged)
        self.ui.actionOpen.triggered.connect(self.openNewFile)
        self.ui.actionRun.triggered.connect(self.run)
        self.ui.actionStep_Over.triggered.connect(self.stepOver)
        self.ui.actionStep_Into.triggered.connect(self.stepInto)

    def updateDisplay(self):
        for i in range(1, 15):
            getattr(self.ui, "reg_"+str(i)).setText(str(self.debugger.register[i]))
        self.ui.ram.setData(''.join(map(chr, self.debugger.ram)))
        self.ui.Z.setState(self.debugger.Z)
        self.ui.N.setState(self.debugger.N)
        self.ui.C.setState(self.debugger.C)
        self.ui.V.setState(self.debugger.V)
        self.ui.editor.setPcLine(self.debugger.getContentLine(self.debugger.pc))

    @pyqtSlot()
    def openNewFile(self):
        filename = QFileDialog.getOpenFileNameAndFilter(self, 'Open File', filter="Compiled/Debug Files (*.out.dbg *.s.out) (*.out.dbg *.out);;All Files (*)")[0]
        if filename != '':
            self.debugger = Debugger.loadFromFile(str(filename), memorysize=0x20)
            self.ui.rom.setData(''.join(map(chr, self.debugger.rom)))
            self.ui.ram.setData(''.join(map(chr, self.debugger.ram)))
            self.ui.editor.setText(self.debugger.fileContent())
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
    def breakpointset(self, line):
        if self.debugger:
            self.debugger.breakpoints.append(self.debugger.getRomAddr(line))

    @pyqtSlot(int)
    def breakpointremoved(self, line):
        if self.debugger:
            self.debugger.breakpoints.remove(self.debugger.getRomAddr(line))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow().show()
    sys.exit(app.exec_())
