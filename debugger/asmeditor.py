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
from PyQt4.Qsci import *


# TODO make lexer work
class LexerAsm(QsciLexerCustom):
    def __init__(self, obj = None):
        QsciLexerCustom.__init__(self, obj)
        self._styles = {
            0: 'Default',
            1: 'Comment',
            2: 'Instruction',
            3: 'Register',
            4: 'Immediate',
            5: 'Label',
            6: 'Data'
        }
        for key, value in self._styles.iteritems():
            setattr(self, value, key)

    def description(self, style):
        return self._styles.get(style, '')

    def language(self):
        return "ASM"

    def defaultColor(self, style):
        if style == self.Default:
            return QtGui.QColor('#000000')
        elif style == self.Comment:
            return QtGui.QColor('#C0C0C0')
        elif style == self.Instruction:
            return QtGui.QColor('#FF8000')
        elif style == self.Register:
            return QtGui.QColor('#00C0C0')
        elif style == self.Immediate:
            return QtGui.QColor('#00CC00')
        elif style == self.Label:
            return QtGui.QColor('#ABCDEF')
        elif style == self.Data:
            return QtGui.QColor('#FEDCBA')
        return Qsci.QsciLexerCustom.defaultColor(self, style)

    def defaultPaper(self, style):
        return QtGui.QColor('#FFFFFF')

    def styleText(self, start, end):
        editor = self.editor()
        if editor is None:
            return

        # scintilla works with encoded bytes, not decoded characters.
        # this matters if the source contains non-ascii characters and
        # a multi-byte encoding is used (e.g. utf-8)
        source = ''
        if end > editor.length():
            end = editor.length()
        if end > start:
            source = bytearray(end - start)
            editor.SendScintilla(editor.SCI_GETTEXTRANGE, start, end, source)
        if not source:
            return

        set_style = self.setStyling
        self.startStyling(start, 0x1f)
        # scintilla always asks to style whole lines
        for line in source.splitlines(False):
            # XXX: insert here!
            line = str(line)

            length = len(line)
            commentStart = line.find(';')

            if commentStart == -1:
                cmd = line
            else:
                cmd = line[:commentStart]

            pos = 0
            if cmd[-1:] == ':':
                set_style(len(cmd), self.Label)
                pos += len(cmd)

            firstSpace = cmd.find(' ', pos)
            if firstSpace == -1:
                firstSpace = len(cmd) - pos

            set_style(firstSpace, self.Instruction)
            pos += firstSpace + 1

            while pos < len(cmd):
                if cmd[pos] in '$#.':
                    if cmd[pos] == '$':
                        style = self.Register
                    elif cmd[pos] == '#':
                        style = self.Immediate
                    else:
                        style = self.Label
                    
                    start = pos
                    while cmd[pos:pos+1] not in ', ':
                        pos += 1
                    set_style(pos-start+1, style)
                else:
                    set_style(1, self.Default)
                    pos += 1

            if commentStart != -1:
                set_style(length - commentStart, self.Comment)
            set_style(1, self.Default) # for the newline, don't forget this!


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
        self.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#F00"), self.ARROW_MARKER_NUM)
        self.SendScintilla(QsciScintilla.SCI_SETCARETLINEVISIBLE, True)
        self.SendScintilla(QsciScintilla.SCI_SETCARETSTYLE, QsciScintilla.CARETSTYLE_INVISIBLE)
        self.SendScintilla(QsciScintilla.SCI_GOTOLINE, -1)

        # set asm lexer
        # TODO does not work yet :/
        self.lexer = LexerAsm(self)
        self.lexer.setDefaultFont(font)
        self.setLexer(self.lexer)
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
