import ast

from ..misc import tools
from .data import Data
from ..errors import EncodingError


class AsciiData(Data):
    def __init__(self, text, binary, inner=None):
        Data.__init__(self, text, binary, inner)
        self.size = len(binary)

    start = ".ascii "

    @classmethod
    def getBinarysize(cls, arg):
        data = arg[len(cls.start):]
        return len(data) * 8

    @classmethod
    def fromText(cls, arg, state):
        ex = EncodingError(arg, "is not a valid %s" % cls.__name__)
        if not cls.isValidText(arg):
            raise ex
        try:
            data = ast.literal_eval(arg[len(cls.start):])
        except SyntaxError:
            raise ex
	if not isinstance(data, str):
            raise ex

        binary = ''.join(tools.tobin(ord(byte), width=8) for byte in data)
        return cls(arg, binary)

    @classmethod
    def isValidBinary(cls, arg):
        return True

    @classmethod
    def fromBinary(cls, arg, state):
        rest = arg
        result = cls.start
        while rest:
            byte, rest = rest[:8], rest[8:]
            result += chr(int(byte, base=2))
        return result
