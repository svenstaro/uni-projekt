from operands import Operand, Register, Immediate
from errors import EncodingError, DecodingError


class Operand2(Operand):
    immType = None

    @classmethod
    def isValidText(cls, arg):
        return Register.isValidText(arg) or Immediate.isValidText(arg)

    @classmethod
    def fromText(cls, arg, state):
        try:
            if Register.isValidText(arg):
                register = Register.fromText(arg, state)
                return cls(arg, "0" + "0" * (cls.size - 5) + register.binary, register)
            else:
                immediate = cls.immType.fromText(arg, state)
                return cls(arg, "1" + immediate.binary, immediate)
        except Exception, e:
            raise EncodingError(arg, "is not valid operand2", e)

    @classmethod
    def fromBinary(cls, arg, state):
        try:
            if not cls.isValidBinary(arg):
                raise ValueError("Invalid size!")
            if arg.startswith("1"):
                inner = cls.immType.fromBinary(arg[1:], state)
            else:
                inner = Register.fromBinary(arg[-4:], state)
            return cls(inner.text, arg, inner)
        except Exception, e:
            raise DecodingError(arg, "is not a valid operand2", e)

