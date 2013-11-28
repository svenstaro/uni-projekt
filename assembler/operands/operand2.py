# vim: softtabstop=4:expandtab

from operands import Operand, Register, Immediate16
from errors import EncodingError, DecodingError
import re


class Operand2(Operand):
    size = 17

    def encodable(self):
        return Register(self.arg).encodable() or Immediate16(self.arg).encodable()

    def encode(self):
        try:
            register = Register(self.arg)
            if register.encodable():
                return "0" + register.encode() + "0" * 12

            imm = Immediate16(self.arg)
            if imm.encodable():
                return "1" + imm.encode()
        except Exception, e:
            raise EncodingError(self.arg, "is not valid operand2", e)

    def decode(self):
        try:
            if not self.decodable():
                raise ValueError("Invalid size!")
            if self.arg.startswith("1"):
                return Immediate16(self.arg[1:]).decode()
            return Register(self.arg[1:5]).decode()
        except Exception,e:
            raise DecodingError(self.arg, "is not a valid operand2", e)
