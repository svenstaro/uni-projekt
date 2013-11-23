# vim: softtabstop=4:expandtab

import myhdl
from operands import Operand


class Immediate(Operand):
    @staticmethod
    def isA(arg):
        return arg.startswith("#")

    @staticmethod
    def encodeGeneric(arg, maxSize):
        ex = ValueError(arg, "is not a valid %s-bit Immediate" % maxSize)
        if not Immediate.isA(arg):
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
    def decodeGeneric(arg, size):
        # TODO Implement
        raise NotImplementedError()


class Immediate16(Immediate):
    def encode(arg):
        return super.encodeGeneric(arg, 16)

    def decode(arg):
        return super.decodeGeneric(arg, 16)
