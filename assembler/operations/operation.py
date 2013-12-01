from structure import Structure
from errors import EncodingError
import re


class Operation(Structure):
    size = 4
    opcodes = None
    argTypes = None

    def isCommand(self, command):
        return self.opcodes.has_key(command)

    def encodable(self):
        (command, _) = self.splitOperation()
        return self.isCommand(command)

    def buildEncodedOperation(self, command, args):
        return self.opcodes[command] + "".join(args)

    def encode(self):
        try:
            (command, args) = self.splitOperation()
            args = [converter(arg).encode() for (converter, arg) in zip(self.argTypes, args)]
            return self.buildEncodedOperation(command, args)
        except Exception, e:
            raise EncodingError("Not a valid %s: " % type(self).__name__, self.arg, e)

    def splitOperation(self):
        (command, arguments) = self.arg.split(" ", 1)
        args = [arg.strip() for arg in arguments.split(",")]
        if not len(args) is len(self.argTypes):
            raise ValueError("Invalid number of arguments:", self.arg)
        return (command, args)

    @staticmethod
    def joinOperation(opname, args):
        return opname + " " + ", ".join(args)

    def decodable(self):
        if not re.match("^[01]{32}$",self.arg):
            return False
        for opcode in self.opcodes.values():
            if self.arg.startswith(opcode):
                return True

    def decodeOpname(self):
        opname = (key for key, val in self.opcodes.items() if self.arg.startswith(val)).next()
        return opname, self.arg[len(self.opcodes[opname]):]

    def decodeArguments(self, remainder):
        args = []
        for argType in self.argTypes:
            current = remainder[0:argType.size]
            args += [argType(current).decode()]
            remainder = remainder[argType.size:]
        return args

    def decode(self):
        opname, remainder = self.decodeOpname()
        args = self.decodeArguments(remainder)
        return Operation.joinOperation(opname, args)
