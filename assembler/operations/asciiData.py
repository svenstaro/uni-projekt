from errors import EncodingError
from operations import Operation
import myhdl


class AsciiData(Operation):
    def __init__(self, arg, position):
        Operation.__init__(self, arg, position)
        self.size = len(arg)

    start = ".ascii "

    def encodable(self):
        return self.arg.startswith(self.start)

    def encode(self):
        if not self.encodable():
            raise EncodingError(self.arg, "is not a valid AsciiData")
        data = self.arg[len(self.start):] + "\0"
        paddinglen = (- len(data)) % 4
        self.size = len(data) + paddinglen

        return ''.join(myhdl.bin(ord(byte), width=8) for byte in data) + "0"*8*paddinglen

    def decodable(self):
        return True

    def decode(self):
        rest = self.arg
        result = ".ascii "
        while rest:
            byte, rest = rest[:8], rest[8:]
            result += chr(int(byte, base=2))
        return result.rstrip("\0")
