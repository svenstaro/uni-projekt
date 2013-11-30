#!/usr/bin/env python

from assembler import *

if __name__ == '__main__':
    with open("out", "rb") as f:
        with open("decoded", "w") as out:
            out.write(decodeCommandStream(readStream(f)))