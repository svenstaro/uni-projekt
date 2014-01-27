from qhexedit import QHexEdit, Decoder
from assembler import getTextOfCommand

class MemoryViewer(QHexEdit):
    def __init__(self, parent):
        super(MemoryViewer, self).__init__(parent)
