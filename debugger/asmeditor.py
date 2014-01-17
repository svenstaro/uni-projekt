#-------------------------------------------------------------------------
# qsci_simple_pythoneditor.pyw
#
# QScintilla sample with PyQt
#
# Eli Bendersky (eliben@gmail.com)
# This code is in the public domain
#-------------------------------------------------------------------------
from PyQt4 import Qsci, QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciLexerCustom


# TODO make lexer work
class LexerAsm(Qsci.QsciLexerCustom):
    def __init__(self, obj = None):
        Qsci.QsciLexerCustom.__init__(self, obj)
        self.sci = None
        self.plainFont = QtGui.QFont()
        self.plainFont.setPointSize(10)
        self.plainFont.setFamily('Courier')
        self.marginFont = QtGui.QFont()
        self.marginFont.setPointSize(10)
        self.marginFont.setFamily('Courier')
        self.boldFont = QtGui.QFont()
        self.boldFont.setPointSize(10)
        self.boldFont.setFamily('Courier')
        self.boldFont.setBold(True)
        self.styles = [
            Qsci.QsciStyle(0, QtCore.QString("mov"), QtGui.QColor("#000000"), QtGui.QColor("#ffffff"), self.plainFont, True),
            Qsci.QsciStyle(1, QtCore.QString("add"), QtGui.QColor("#008000"), QtGui.QColor("#eeffee"), self.marginFont, True),
            Qsci.QsciStyle(2, QtCore.QString("jmp"), QtGui.QColor("#000080"), QtGui.QColor("#ffffff"), self.boldFont, True),
            Qsci.QsciStyle(3, QtCore.QString("string"), QtGui.QColor("#800000"), QtGui.QColor("#ffffff"), self.marginFont, True),
            Qsci.QsciStyle(4, QtCore.QString("atom"), QtGui.QColor("#008080"), QtGui.QColor("#ffffff"), self.plainFont, True),
            Qsci.QsciStyle(5, QtCore.QString("macro"), QtGui.QColor("#808000"), QtGui.QColor("#ffffff"), self.boldFont, True),
            Qsci.QsciStyle(6, QtCore.QString("error"), QtGui.QColor("#000000"), QtGui.QColor("#ffd0d0"), self.plainFont, True)]

    def description(self, ix):
        for i in self.styles:
            if i.style() == ix:
                return QtCore.QString(i.description())
        return QtCore.QString("")

    def setEditor(self, sci):
        self.sci = sci
        Qsci.QsciLexerCustom.setEditor(self, sci)

    def styleText(self, start, end):
        print("LexerErlang.styleText(%d,%d)" % (start, end))
        lines = self.getText(start, end)
        offset = start
        self.startStyling(offset, 0)
        print("startStyling()")
        for i in lines:
            if i == "":
                self.setStyling(1, self.styles[0])
                print("setStyling(1)")
                offset += 1
                continue
            if i[0] == '%':
                self.setStyling(len(i)+1, self.styles[1])
                print("setStyling(%)")
                offset += len(i)+1
                continue
            self.setStyling(len(i)+1, self.styles[0])
            print("setStyling(n)")
            offset += len(i)+1

    def getText(self, start, end):
        data = self.sci.text()
        print("LexerErlang.getText(): " + str(len(data)) + " chars")
        return data[start:end].split('\n')


class AsmEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(AsmEditor, self).__init__(parent)

        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(14)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("0000"))
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.on_margin_clicked)
        self.markerDefine(QsciScintilla.RightArrow,
            self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#000"),
            self.ARROW_MARKER_NUM)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffeedd"))

        # set asm lexer
        # TODO does not work yet :/
        lexer = LexerAsm()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

    @pyqtSlot(int, int, Qt.KeyboardModifier)
    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)
