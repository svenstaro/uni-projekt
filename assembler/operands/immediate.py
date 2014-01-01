import string
from ..misc import tools
from .operand import Operand
from ..errors import EncodingError, DecodingError


def Immediate(size):
    class Immediate(Operand):

        start = "#"

        @classmethod
        def fromText(cls, arg, state):
            ex = EncodingError(arg, "is not a valid %s-bit Immediate" % cls.size)
            if not cls.isValidText(arg):
                raise ex
            binary = tools.immediate2binary(arg[1:], cls.size)
            if not binary:
                raise ex
            return cls(arg, binary)

        @staticmethod
        def negate(bitstring):
            return bitstring.translate(string.maketrans("01", "10"))

        @classmethod
        def fromBinary(cls, arg, state):
            ex = DecodingError(arg, "is not a valid %s-bit Immediate" % cls.size)

            if not cls.isValidBinary(arg):
                raise ex

            number = int(arg, base=2) if arg[0] == "0" else ~int(Immediate.negate(arg), base=2)

            return cls("#" + str(number), arg)
    return type("Immediate"+str(size),(Immediate,),dict(size=size))
