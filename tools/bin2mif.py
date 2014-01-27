#! /usr/bin/env python2.7

import struct
import sys
import os
from myhdl import bin  # TODO remove myhdl dep
from argparse import ArgumentParser

depth = 256
width = 32
addr_radix = 'DEC'
data_radix = 'HEX'

def convert(data, fout):
    print >>fout, 'DEPTH = %d;' % depth
    print >>fout, 'WIDTH = %d;' % width
    print >>fout, 'ADDRESS_RADIX = %s;' % addr_radix
    print >>fout, 'DATA_RADIX = %s;' % data_radix
    print >>fout, 'CONTENT'
    print >>fout, 'BEGIN'
    for i in range(0, len(data)):
        print >>fout, '%-3d : %s;' % (i*4, hex(data[i])[2:].zfill(8))
    print >>fout, 'END;'
    return 0

if __name__ == '__main__':
    parser = ArgumentParser(description='Bin2Mif converter')
    parser.add_argument('fin', type=str, nargs=1, help='input file')
    parser.add_argument('fout', type=str, nargs='?', default='-', help='output')

    args = parser.parse_args()
    with open(args.fin[0]) as f:
        size = os.path.getsize(f.name)//4
        data = struct.unpack('>' + "I"*size, f.read(4*size))

    fh = open(args.fout, 'w') if args.fout != '-' else sys.stdout

    try:
        sys.exit(convert(data, fh))
    finally:
        if fh is not sys.stdout:
            fh.close()
