import re

from structure import Structure
from errors import EncodingError
from operands import Ignore

class Operation(Structure):
    def __init__(self, arg, position):
        Structure.__init__(self, arg)
        self.position = position

    size = 4
    opcodes = None
    argTypes = None

    def isCommand(self, command):
        return self.opcodes.has_key(command)

    def encodable(self):
        try:
            command = self.splitOperation()[0]
            return self.isCommand(command)
        except ValueError:
            return False

    def buildEncodedOperation(self, command, args):
        return self.opcodes[command] + "".join(args)

    def encode(self):
        try:
            (command, args) = self.splitOperation()
            encodedArgs = []
            count = 0
            for argType in self.argTypes:
                encodedArgs.append(argType(args[count]).encode())
                if not issubclass(argType, Ignore):
                    count += 1

            return self.buildEncodedOperation(command, encodedArgs)
        except Exception, e:
            raise EncodingError("Not a valid %s: " % type(self).__name__, self.arg, e)

    def splitOperation(self):
        splittedLine = self.arg.split(" ", 1)
        command = splittedLine[0]

        if len(splittedLine) is 1:
            return command, []

        args = [arg.strip() for arg in splittedLine[1].split(",")]
        if not len(args) is len([argType for argType in self.argTypes if not issubclass(argType, Ignore)]):
            raise ValueError("Invalid number of arguments:", self.arg)
        return command, args

    @staticmethod
    def joinOperation(opname, args):
        return opname + " " + ", ".join(args)

    def decodable(self):
        if not re.match("^[01]{32}$", self.arg):
            return False
        for opcode in self.opcodes.values():
            if self.arg.startswith(opcode) and self.argumentsDecodable(self.arg[len(opcode):]):
                return True
        return False

    def argumentsDecodable(self, remainder):
        for argType in self.argTypes:
            current, remainder = remainder[:argType.size], remainder[argType.size:]
            if not argType(current).decodable():
                return False
        return True


    def decodeOpname(self):
        opname = (key for key, val in self.opcodes.items() if self.arg.startswith(val)).next()
        return opname, self.arg[len(self.opcodes[opname]):]

    def decodeArguments(self, remainder):
        args = []
        for argType in self.argTypes:
            current, remainder = remainder[:argType.size], remainder[argType.size:]
            if not issubclass(argType, Ignore):
                args += [argType(current).decode()]
        return args

    def decode(self):
        opname, remainder = self.decodeOpname()
        args = self.decodeArguments(remainder)
        return Operation.joinOperation(opname, args)

