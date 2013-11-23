# vim: softtabstop=4:expandtab

from operands import Operand
from errors import EncodingError, DecodingError
import re, string, myhdl


class Immediate(Operand):
    @staticmethod
    def encodable(arg):
        return arg.startswith("#")

    @staticmethod
    def encodeGeneric(arg, maxSize):
        ex = EncodingError(arg, "is not a valid %s-bit Immediate" % maxSize)
        if not Immediate.encodable(arg):
            raise ex
        number = arg[1:]

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
            raise ex

        if not -2 ** (maxSize - 1) <= result <= 2 ** (maxSize - 1) - 1:
            raise ex

        return myhdl.bin(result, width=maxSize)

    @staticmethod
    def decodableGeneric(arg,size):
        return re.match("^[01]{%s}$" % size, arg)

    @staticmethod
    def negate(arg):
        return arg.translate(string.maketrans("01","10"))

    @staticmethod
    def decodeGeneric(arg, size):
        ex = DecodingError(arg, "is not a valid %s-bit Immediate" % size)

        if not Immediate.decodableGeneric(arg, size):
            raise ex

        if arg[0] is "0":
            return int(arg, base=2)
        else:
            return ~int(Immediate.negate(arg), base=2)


class Immediate16(Immediate):
    @staticmethod
    def encode(arg):
        return super.encodeGeneric(arg, 16)

    @staticmethod
    def decodable(arg):
        return super.decodableGeneric(arg, 16)

    @staticmethod
    def decode(arg):
        return super.decodeGeneric(arg, 16)
