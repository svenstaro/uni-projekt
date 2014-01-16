from .operations import getOperations
from .misc import tools
from .data import getData
from .errors import EncodingError, DecodingError
from .misc.state import EncodingState, DecodingState
from .data import WordData

def parseCommand(line, ops, encode=True):
    for op in ops:
        if encode and op.isValidText(line):
            return op
        elif not encode and op.isValidBinary(line):
            return op


def getTextOfEncodedCommand(bytes):
    binary = ""
    for byte in bytes:
        binary += bin(ord(byte))[2:].zfill(8)
    return getTextOfCommand(binary)


def getTextOfCommand(binary):
    try:
        return parseCommand(binary, getOperations(), encode=False).fromBinary(binary, None).text
    except:
        return None


def isLabel(s):
    if not s.endswith(":"):
        return False
    return tools.labelPattern.match(s[:-1])


def stripLine(line):
    in_string = False
    result = ""
    i = 0
    while i < len(line):
        char = line[i]
        if char == ';' and not in_string:
            return result
        if char == "\\":
            result += line[i:i+1]
            i += 2
            continue
        if char == "\"":
            in_string = not in_string
        result += char
        i += 1
    if in_string:
        raise ValueError(line)  # TODO: invalid count of "
    return result.strip(" \r\n")

def encodeCommandStream(lines):
    labels = {}
    ops = getOperations()
    data = getData()

    pos = 0
    for line in lines:
        line = stripLine(line)
        if line == "":
            continue
        elif isLabel(line):
            parseLabel(line, labels, pos)
        elif line[0] == ".":
            size = parseData(line, data, None, sizeOnly=True)
            if size:
                pos += size / 8
            else:
                raise EncodingError(line, "Invalid instruction")
        else:
            pos += 4

    stream = ""
    pos = 0

    for (number, line) in enumerate(lines):
        line = stripLine(line)
        if not line:
            continue
        elif isLabel(line):  # Label
            continue
        elif line[0] == ".":
            d = parseData(line, data, EncodingState(labels, pos))
            stream += d.binary
            pos += d.size / 8
        else:
            try:
                op = parseCommand(line, ops, encode=True)
                stream += op.fromText(line, EncodingState(labels, pos)).binary
                pos += op.size / 8
            except:
                raise EncodingError(line, "Invalid instruction")
    return stream


def decodeCommandStream(stream):
    ops = getOperations()
    pos = 0
    result = ""
    while stream:
        word, stream = stream[:32], stream[32:]
        op = parseCommand(word, ops, encode=False)
        if op is None:
            op = WordData
            word = word.ljust(32, "0")
        line = op.fromBinary(word, None).text
        result += line + "\n"
    return result



def parseLabel(line, labels, pos):
    labelname = line[0:-1]
    if labelname in labels:
        raise ValueError(labelname, "Label appeared twice!")
    labels[labelname] = pos

def parseData(line, data, state, sizeOnly=False):
    for d in data:
        if d.isValidText(line):
            if sizeOnly:
                return d.getBinarysize(line)
            else:
                return d.fromText(line, state)
