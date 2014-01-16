#!/usr/bin/env python2

import struct
import sys
import os
import argparse

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
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="create debug file",
                        action="store_true")
    parser.add_argument("filename", help="name of source file")
    args = parser.parse_args()

    fin = os.open(args.filename, os.O_RDONLY, 0777)
    content = ""
    while True:
        read = os.read(fin, 4096)
        if len(read) == 0:
            break
        content += read
    os.close(fin)

    lines = content.split('\n')

    stream, debug_info = encodeCommandStream(lines)

    fout = os.open(args.filename + ".out", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0644)
    writeStream(fout, stream)
    os.close(fout)

    if args.debug:
        fout = os.open(args.filename + ".out.dbg", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0644)
        os.write(fout, debug_info)
        os.close(fout)


    return 0


def target(*args):
    return entry_point, None

if __name__ == '__main__':
    entry_point(sys.argv)
