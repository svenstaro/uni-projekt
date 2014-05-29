#! /usr/bin/env python2.7

import sys
from PIL import Image

width = 1
addr_radix = 'DEC'
data_radix = 'BIN'

def convert(data, fout):
    print >>fout, 'DEPTH = %d;' % (len(data)/3)
    print >>fout, 'WIDTH = %d;' % width
    print >>fout, 'ADDRESS_RADIX = %s;' % addr_radix
    print >>fout, 'DATA_RADIX = %s;' % data_radix
    print >>fout, 'CONTENT'
    print >>fout, 'BEGIN'
    for i in range(0, len(data)):
        print >>fout, "%d : %s;" % (i, bin(data[i])[2:])
    print >>fout, 'END;'


if __name__ == '__main__':
    im = Image.open(sys.argv[1])
    if im.size == (800,480):
        with open('out.mif', 'wb') as output:
            data = im.tobytes()
            convert(map(ord, data), output)
    else:
        print "Noe, Peter!"

