import re

from ..misc.structure import Structure
from ..errors import EncodingError
from ..operands import Ignore, Operand
from ..operands.opcodes import OpcodesBaseClass


class Operation(Structure):

    size = 32
    opcodes = None
    structure = None

    @classmethod
    def isCommand(cls, cmd):
        return cmd in cls.opcodes

    @classmethod
    def isValidText(cls, arg):
        try:
            command = cls.splitOperation(arg)[0]
            return cls.isCommand(command)
        except ValueError:
            return False

    @staticmethod
    def findArgPosition(line, n):
        pos = line.find(' ')
        for _ in range(n):
            pos = line.find(',', pos) + 1
        while line[pos] == ' ':
            pos += 1
        return pos
 

    @classmethod
    def fromText(cls, line, state):
        (command, args) = cls.splitOperation(line)
        binary = ""
        encodedArgs = []
        count = 0
        for part in cls.structure:
            if issubclass(part, OpcodesBaseClass):
                binary += part.fromText(command, None).binary
            elif issubclass(part, Ignore):
                binary += part.fromText(None, None).binary
            elif issubclass(part, Operand):
                try:
                    arg = part.fromText(args[count], state)
                except EncodingError as e:
                    position = cls.findArgPosition(line, count)
                    s = '-'*position + '^'
                    raise EncodingError(line + '\n' + s, "Not a valid %s (%s)" % (cls.__name__, e.errString))
                encodedArgs.append(arg)
                binary += arg.binary
                count += 1
            else:
                raise EncodingError(line, "Not a valid %s" % cls.__name__)

        return cls(line, binary, encodedArgs)

    @classmethod
    def splitOperation(cls, arg):
        splittedLine = arg.split(" ", 1)
        command = splittedLine[0]

        if len(splittedLine) is 1:
            return command, []

        args = [arg.strip() for arg in splittedLine[1].split(",")]
        if not len(args) is len([argType for argType in cls.structure
                                 if issubclass(argType, Operand) and not issubclass(argType, Ignore)]):
            raise ValueError("Invalid number of arguments:", arg)
        return command, args

    @staticmethod
    def joinOperation(opname, args):
        return opname + " " + ", ".join(args)

    @classmethod
    def isValidBinary(cls, arg):
        if not re.match("^[01]{32}$", arg):
            return False
        remainder = arg
        for part in cls.structure:
            current, remainder = remainder[:part.size], remainder[part.size:]
            if not part.isValidBinary(current):
                return False
        return True

    @classmethod
    def fromBinary(cls, arg, state):
        remainder = arg
        opname = ""
        args = []
        for part in cls.structure:
            current, remainder = remainder[:part.size], remainder[part.size:]
            if issubclass(part, OpcodesBaseClass):
                opname = part.fromBinary(current, state)
            elif issubclass(part, Ignore):
                pass
            elif issubclass(part, Operand):
                args.append(part.fromBinary(current, state))

        text = Operation.joinOperation(opname, [arg.text for arg in args])
        return cls(text, arg, args)

