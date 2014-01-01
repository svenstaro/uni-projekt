from .data import Data
from ..errors import EncodingError
from .. import tools
import ast


class BinaryData(Data):

    @classmethod
    def fromText(cls, arg, state):
        ex = EncodingError(arg, "is not a valid %s" % cls.__name__)
        if not cls.isValidText(arg):
            raise ex
        data = arg[len(cls.start):]
        if tools.labelPattern.match(data):
            number = tools.label2immediate(data, state) + state.position
	else:
            try:
                number = ast.literal_eval(data)
            except SyntaxError:
                raise ex
            if not isinstance(number, (int,long)):
                raise ex
        if not -2 ** (cls.size - 1) <= number <= 2 ** cls.size - 1:
            raise ex
        binary = tools.tobin(number, cls.size)
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
