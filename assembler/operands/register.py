# vim: softtabstop=4:expandtab

import re

from operands import Operand
from errors import EncodingError, DecodingError


class Register(Operand):
    @staticmethod
    def encodable(arg):
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
    def decodable(arg):
        return re.match("^[01]{4}$", arg)

    @staticmethod
    def decode(arg):
        # TODO Do error checking
        ex = DecodingError(arg, "is not a valid encoded register")

        if not Register.decodable(arg):
            raise ex

        try:
            return "$" + str(int(arg, base=2))
        except:
            raise ex

