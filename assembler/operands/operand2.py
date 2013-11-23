# vim: softtabstop=4:expandtab

from operands import Operand, Register, Immediate16
from errors import EncodingError, DecodingError


class Operand2(Operand):
    @staticmethod
    def encodable(arg):
        return Register.encodable(arg) or Immediate16.encodable(arg)

    @staticmethod
    def encode(arg):
        try:
            if Register.encodable(arg):
                return "0" + Register.encode(arg) + "0" * 12

            if Immediate16.encodable(arg):
                return "1" + Immediate16.encode(arg)
        except: # TODO: Capture error
            raise EncodingError(arg, "is not valid operand2")

    @staticmethod
    def decode(arg):
        # TODO Do error checking
        if arg.startswith("1"):
            return Immediate16.decode(arg[1:])
        return Register.decode(arg[1:4])
