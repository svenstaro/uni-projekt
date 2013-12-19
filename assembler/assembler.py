#!/usr/bin/env python2

from operations import getOperations
from state import EncodingState, DecodingState
from errors import EncodingError
import struct
import tools
import sys
import os
from data import getData
from data import WordData
import string


def isLabel(s):
    if not s.endswith(":"):
        return False
    return tools.labelPattern.match(s[:-1])


def encodeCommandStream(lines):
    labels = {}
    ops = getOperations()
    data = getData()

    pos = 0
    for line in lines:
        line = line.strip(" \r\n").split(";", 1)[0]
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
        line = line.strip(" \r\n").split(";", 1)[0]
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

def parseCommand(line, ops, encode=True):
    for op in ops:
        if encode and op.isValidText(line):
            return op
        elif not encode and op.isValidBinary(line):
            return op


def writeStream(fd, stream):
    while stream:
        firstbyte, stream = stream[0:8], stream[8:]

        binary = struct.pack("B", int(firstbyte, base=2))
        os.write(fd, binary)


def readStream(f):
    stream = ""
    for binary in f.read():
        byte = struct.unpack("B", binary)[0]
        stream += tools.tobin(byte, width=8)
    return stream


def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        return 1

    fin = os.open(filename, os.O_RDONLY, 0777)
    content = ""
    while True:
        read = os.read(fin, 4096)
        if len(read) == 0:
            break
        content += read
    os.close(fin)

    lines = content.split('\n')

    stream = encodeCommandStream(lines)

    fout = os.open(filename + ".out", os.O_WRONLY | os.O_CREAT, 0644)
    writeStream(fout, stream)
    os.close(fout)

    return 0


def target(*args):
    return entry_point, None

if __name__ == '__main__':
    entry_point(sys.argv)
