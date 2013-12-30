from .data import Data
from errors import EncodingError
import tools


class BinaryData(Data):

    @classmethod
    def fromText(cls, arg, state):
        if not cls.isValidText(arg):
            raise EncodingError(arg, "is not a valid %s" % cls.__name__)
        data = arg[len(cls.start):]
        number = str(tools.label2immediate(data, state) + state.position) if tools.labelPattern.match(data) else data
        binary = tools.immediate2binary(number, cls.size)
        if not binary:
            raise EncodingError(arg, "is not a valid %s" % cls.__name__)
        return cls(arg, binary)

    @classmethod
    def isValidBinary(cls, arg):
        return len(arg) == cls.size

    @classmethod
    def fromBinary(cls, arg, state):
        text = cls.start + hex(int(arg, base=2))
        return cls(text, arg)


class WordData(BinaryData):
    size = 32
    start = ".word "


class HalfData(BinaryData):
    size = 16
    start = ".half "


class ByteData(BinaryData):
    size = 8
    start = ".byte "
