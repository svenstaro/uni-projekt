from operands import Operand, Register, Immediate
from errors import EncodingError, DecodingError


class Operand2(Operand):
    def encodable(self):
        return Register(self.arg, self.state).encodable() or Immediate(self.arg, self.state, self.size - 1).encodable()

    def encode(self):
        try:
            register = Register(self.arg, self.state)
            if register.encodable():
                return "0" + register.encode() + "0" * (self.size - 5)

            imm = Immediate(self.arg, self.state, self.size - 1)
            if imm.encodable():
                return "1" + imm.encode()
        except Exception, e:
            raise EncodingError(self.arg, "is not valid operand2", e)

    def decode(self):
        try:
            if not self.decodable():
                raise ValueError("Invalid size!")
            if self.arg.startswith("1"):
                return Immediate(self.arg[1:], self.state, self.size - 1).decode()
            return Register(self.arg[1:5], self.state).decode()
        except Exception, e:
            raise DecodingError(self.arg, "is not a valid operand2", e)

