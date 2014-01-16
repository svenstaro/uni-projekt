from myhdl import *
from math import log
from assembler import getTextOfCommand


def pseudorom(clk, oe, cs, addr, dout, mem):
    """This is a pseudorom with delay
    """

    o = dout.driver()

    @always_comb
    def read():
        o.next = None

        if cs and oe:
            assert int(addr)//4 < len(mem)

            if __debug__:
                a = bin(mem[int(addr)//4], width=32)
                print "ROM (" + '0x%02X' % addr + "): " + ' '.join(map(lambda *xs: ''.join(xs), *[iter(a)]*8)) + ' | ' + str(getTextOfCommand(a))

            o.next = mem[int(addr)//4]

    return read
