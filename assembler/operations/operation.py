import re

from structure import Structure
from errors import EncodingError
from operands import Ignore


class Operation(Structure):

    size = 32
    opcodes = None
    argTypes = None

    @classmethod
    def isCommand(cls, command):
        return command in cls.opcodes

    @classmethod
    def isValidText(cls, arg):
        try:
            command = cls.splitOperation(arg)[0]
            return cls.isCommand(command)
        except ValueError:
            return False

    @classmethod
    def buildEncodedOperation(cls, command, args):
        return cls.opcodes[command] + "".join(args)

    @classmethod
    def fromText(cls, line, state):
        try:
            (command, args) = cls.splitOperation(line)
            encodedArgs = []
            count = 0
            for argType in cls.argTypes:
                encodedArgs.append(argType.fromText(args[count], state))
                if not issubclass(argType, Ignore):
                    count += 1

            return cls(line, cls.buildEncodedOperation(command, [arg.binary for arg in encodedArgs]), encodedArgs)
        except Exception, e:
            raise EncodingError("Not a valid %s: " % cls.__name__, line, e)

    @classmethod
    def splitOperation(cls, arg):
        splittedLine = arg.split(" ", 1)
        command = splittedLine[0]

        if len(splittedLine) is 1:
            return command, []

        args = [arg.strip() for arg in splittedLine[1].split(",")]
        if not len(args) is len([argType for argType in cls.argTypes if not issubclass(argType, Ignore)]):
            raise ValueError("Invalid number of arguments:", arg)
        return command, args

    @staticmethod
    def joinOperation(opname, args):
        return opname + " " + ", ".join(args)

    @classmethod
    def isValidBinary(cls, arg):
        if not re.match("^[01]{32}$", arg):
            return False
        for opcode in cls.opcodes.values():
            if arg.startswith(opcode) and cls.argumentsDecodable(arg[len(opcode):]):
                return True
        return False

    @classmethod
    def argumentsDecodable(cls, remainder):
        for argType in cls.argTypes:
            current, remainder = remainder[:argType.size], remainder[argType.size:]
            if not argType.isValidBinary(current):
                return False
        return True

    @classmethod
    def decodeOpname(cls, arg):
        opname = (key for key, val in cls.opcodes.items() if arg.startswith(val)).next()
        return opname, arg[len(cls.opcodes[opname]):]

    @classmethod
    def decodeArguments(cls, remainder, state):
        args = []
        for argType in cls.argTypes:
            current, remainder = remainder[:argType.size], remainder[argType.size:]
            if not issubclass(argType, Ignore):
                args += [argType.fromBinary(current, state)]
        return args

    @classmethod
    def fromBinary(cls, arg, state):
        opname, remainder = cls.decodeOpname(arg)
        args = cls.decodeArguments(remainder, state)
        #
        text = Operation.joinOperation(opname, [arg.text for arg in args])
        return cls(text, arg, args)

