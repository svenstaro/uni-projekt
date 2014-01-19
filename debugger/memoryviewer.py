from qhexedit import QHexEdit, Decoder
from assembler import getTextOfCommand

class MemoryViewer(QHexEdit):
    def __init__(self, parent):
        super(MemoryViewer, self).__init__(parent)


class AsmDecoder(Decoder):
    def decode(self, data, pos):
        res = None
        if pos <= data.size() - 4:
            com = ord(data[pos]) << 24 | ord(data[pos+1]) << 16 | ord(data[pos+2]) << 8 | ord(data[pos+3])
            res = getTextOfCommand(str(bin(com)[2:].zfill(32)))

        return res if res else ""

    def skipBytes(self):
        return 4

