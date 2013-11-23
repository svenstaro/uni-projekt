# vim: softtabstop=4:expandtab

from operands import Operand
from exceptions import EncodingError, DecodingError


class Register(Operand):
    @staticmethod
    def isA(arg):
        return arg.startswith("$")

    @staticmethod
    def encode(arg):
        ex = EncodingError(arg, "is not a valid register")

        if not arg.startswith("$"):
            raise ex

        try:
            result = int(arg[1:])
        except ValueError:
            raise ex

        if not 0 <= result <= 15:
            raise ex

        return format(result, "04b")

    @staticmethod
    def decode(arg):
        # TODO Do error checking
        ex = DecodingError(arg, "is not a valid encoded register")

        return "$" + int(arg, base=2)

