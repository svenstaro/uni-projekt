#!/usr/bin/env python

import re
from operations import getOperations
import struct, myhdl

def encodeCommandStream(f):
    labels = {}
    ops = getOperations(labels)

    labelPattern = re.compile("^(?P<label>\.[a-zA-Z0-9_-]+):$")
    def parseLabel(line, labels, pos):
        labelname = labelPattern.match(line).group('label')
        if labels.has_key(labelname):
            raise ValueError(labelname, "Label appeared twice!")
        labels[labelname] = pos

    cmds = []
    pos = 0
    for (number, line) in enumerate(f):
        line = line.strip()
        if not line or line[0] is "#":
            continue
        if labelPattern.match(line):  # Label
            parseLabel(line, labels, pos)
        else:
            cmd = parseCommand(line, ops, pos, encode=True)
            cmds.append(cmd)
            pos += cmd.size

    stream = ""
    for cmd in cmds:
        stream += cmd.encode()
    return stream

def decodeCommandStream(stream):
    labels = {}
    ops = getOperations(labels)
    pos = 0
    result = ""
    while stream:
        word, stream = stream[:32], stream[32:]
        cmd = parseCommand(word, ops, pos, encode=False)
        line = cmd.decode()
        result += line + "\n"
    return result

def parseCommand(line, ops, pos, encode=True):
    for op in ops:
        cmd = op(line, pos)
        if encode and cmd.encodable():
            return cmd
        elif not encode and cmd.decodable():
            return cmd

def writeStream(f, stream):
    while stream:
        firstbyte, stream = stream[0:8], stream[8:]

        binary = struct.pack("B", int(firstbyte, base=2))
        f.write(binary)

def readStream(f):
    stream = ""
    for binary in f.read():
        byte = struct.unpack("B", binary)[0]
        stream += myhdl.bin(byte, width=8)
    return stream

if __name__ == '__main__':
    with open("testfile") as f:
        with open("out", "wb") as out:
            writeStream(out, encodeCommandStream(f))