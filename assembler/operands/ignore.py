from .operand import Operand


class Ignore(Operand):
    @classmethod
    def isValidText(cls, arg):
        return True

    @classmethod
    def fromBinary(cls, arg, state):
        raise DecodingError(arg, "is a %s, which can not be decoded!" % cls.__name__)
