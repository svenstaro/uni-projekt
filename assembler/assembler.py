#!/usr/bin/env python2

import struct
import sys
import os

sys.path.insert(0, os.path.dirname(__file__) + '/../')
from assembler import encodeCommandStream



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

    fout = os.open(filename + ".out", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0644)
    writeStream(fout, stream)
    os.close(fout)

    return 0


def target(*args):
    return entry_point, None

if __name__ == '__main__':
    entry_point(sys.argv)
