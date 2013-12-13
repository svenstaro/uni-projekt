from .asciiData import AsciiData


class AsciizData(AsciiData):

    start = ".asciiz "

    @classmethod
    def getBinarysize(cls, arg):
        return super(AsciizData, cls).getBinarysize(arg) + 8

    @classmethod
    def fromText(cls, arg, state):
        inner = super(AsciizData, cls).fromText(arg, state)
        return cls(arg, inner.binary + "0"*8, inner)

    @classmethod
    def fromBinary(cls, arg, state):
        inner = super(AsciizData, cls).fromBinary(arg, state)
        return cls(inner.text.rstrip("\0"), arg, inner)
