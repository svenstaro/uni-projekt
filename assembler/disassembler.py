#!/usr/bin/env python

import sys, os

sys.path.insert(0, os.path.dirname(__file__) + '/../')
from assembler import decodeCommandStream


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

    binary = ""
    for byte in content:
        binary += bin(ord(byte))[2:].zfill(8)

    stream = decodeCommandStream(binary)

    fout = os.open(filename + ".dec", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0644)
    os.write(fout, stream)
    os.close(fout)

    return 0


def target(*args):
    return entry_point, None

if __name__ == '__main__':
    entry_point(sys.argv)
