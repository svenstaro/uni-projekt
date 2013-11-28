import re

from operands import Operand
from errors import EncodingError, DecodingError


class Register(Operand):
    def encodable(self):
        return self.arg.startswith("$")

    def encode(self):
        ex = EncodingError(self.arg, "is not a valid register")

        if not self.arg.startswith("$"):
            raise ex

        try:
            result = int(self.arg[1:])
        except ValueError:
            raise ex

        if not 0 <= result <= 15:
            raise ex

        return format(result, "04b")

    def decodable(self):
        return re.match("^[01]{4}$", self.arg)

    def decode(self):
        # TODO Do error checking
        ex = DecodingError(self.arg, "is not a valid encoded register")

        if not self.decodable():
            raise ex

        try:
            return "$" + str(int(self.arg, base=2))
        except:
            raise ex

