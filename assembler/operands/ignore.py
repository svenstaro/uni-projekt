from operand import Operand
from errors import DecodingError


class Ignore(Operand):
    @classmethod
    def isValidText(cls, arg):
        return True

    @classmethod
    def fromText(cls, arg, state):
        return cls(arg, "0"*cls.size)

    @classmethod
    def isValidBinary(cls, arg):
        return arg == "0"*cls.size

    @classmethod
    def fromBinary(cls, arg, state):
        raise DecodingError(arg, "is a %s, which can not be decoded!" % cls.__name__)


class IgnoreRegister(Ignore):
    size = 4