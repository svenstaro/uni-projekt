import string

from operands import Operand
from errors import EncodingError, DecodingError
import tools


class Immediate(Operand):

    start = "#"

    @staticmethod
    def immediate2binary(number, size):
        sign = ""
        if number.startswith("-"):
            sign = "-"
            number = number[1:]
        base = 10
        if number.startswith("0b"):
            base = 2
        elif number.startswith("0x"):
            base = 16
        elif number.startswith("0"):
            base = 8
        try:
            result = int(sign + number, base=base)
        except ValueError:
            return False
        if not -2 ** (size - 1) <= result <= 2 ** (size - 1) - 1:
            return False
        binary = tools.tobin(result, width=size)
        return binary

    @classmethod
    def fromText(cls, arg, state):
        ex = EncodingError(arg, "is not a valid %s-bit Immediate" % cls.size)
        if not cls.isValidText(arg):
            raise ex
        binary = Immediate.immediate2binary(arg[1:], cls.size)
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

class Immediate8(Immediate):
    size = 8

class Immediate16(Immediate):
    size = 16

class Immediate24(Immediate):
    size = 24

class Immediate32(Immediate):
    size = 32
