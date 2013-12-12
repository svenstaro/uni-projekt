from errors import EncodingError
from operation import Operation
import tools

class AsciiData(Operation):
    def __init__(self, arg, state):
        Operation.__init__(self, arg, state)
        self.size = len(arg)
        if self.encodable():
                data = self.arg[len(self.start):] + "\0"
                self.size = len(data) + (- len(data)) % 4

    start = ".ascii "

    def encodable(self):
        return self.arg.startswith(self.start)

    def encode(self):
        if not self.encodable():
            raise EncodingError(self.arg, "is not a valid AsciiData")
        data = self.arg[len(self.start):] + "\0"
        paddinglen = (- len(data)) % 4

        return ''.join(tools.tobin(ord(byte), width=8) for byte in data) + "0"*8*paddinglen

    def decodable(self):
        return True

    def decode(self):
        rest = self.arg
        result = ".ascii "
        while rest:
            byte, rest = rest[:8], rest[8:]
            result += chr(int(byte, base=2))
        return result.rstrip("\0")
