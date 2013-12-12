import string

from operands import Operand
from errors import EncodingError, DecodingError
import tools


class Immediate(Operand):
    def __init__(self, arg, state, size):
        Operand.__init__(self, arg, state)
        self.size = size

    def encodable(self):
        return self.arg.startswith("#")

    def encode(self):
        ex = EncodingError(self.arg, "is not a valid %s-bit Immediate" % self.size)
        if not self.encodable():
            raise ex
        number = self.arg[1:]

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

        if not -2 ** (self.size - 1) <= result <= 2 ** (self.size - 1) - 1:
            raise ex

        return tools.tobin(result, width=self.size)

    @staticmethod
    def negate(bitstring):
        return bitstring.translate(string.maketrans("01", "10"))

    def decode(self):
        ex = DecodingError(self.arg, "is not a valid %s-bit Immediate" % self.size)

        if not self.decodable():
            raise ex

        if self.arg[0] is "0":
            return "#" + str(int(self.arg, base=2))
        else:
            return "#" + str(~int(Immediate.negate(self.arg), base=2))
