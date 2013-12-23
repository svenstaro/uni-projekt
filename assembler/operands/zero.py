from .ignore import Ignore
from errors import DecodingError


def Zero(size):
    class Zero(Ignore):

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

    return type("Zero"+str(size), (Zero,), dict(size=size))