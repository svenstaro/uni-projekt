from operand import Operand
from errors import DecodingError


class Ignore(Operand):
    def encodable(self):
        return True

    def encode(self):
        return "0"*self.size

    def decodable(self):
        return self.arg == "0"*self.size

    def decode(self):
        if not self.decodable():
            raise DecodingError(self.arg, "is not null!")
        return ""


class IgnoreRegister(Ignore):
    size = 4