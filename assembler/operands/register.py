from operands import Operand
from errors import EncodingError, DecodingError


class Register(Operand):
    size = 4
    start = "$"

    @classmethod
    def fromText(cls, arg, state):
        ex = EncodingError(arg, "is not a valid register")

        if not cls.isValidText(arg):
            raise ex

        try:
            result = int(arg[1:])
        except ValueError:
            raise ex

        if not 0 <= result <= 15:
            raise ex

        return cls(arg, format(result, "04b"))

    @classmethod
    def fromBinary(cls, arg, state):
        if not cls.isValidBinary(arg):
            raise DecodingError(arg, "is not a valid encoded register")
        return cls("$" + str(int(arg, base=2)), arg)

