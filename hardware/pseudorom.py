from myhdl import *
from assembler.assembler import getTextOfCommand

def pseudorom(oe, cs, addr, dout, mem):
    """This is a pseudorom
    """

    @always_comb
    def read():
        if cs and oe:
            assert int(addr)//4 < len(mem)

            if __debug__:
                a = bin(mem[int(addr)//4], width=32)
                print "ROM (" + '0x%02X' % addr + "): " + ' '.join(map(lambda *xs: ''.join(xs), *[iter(a)]*8)) + ' | ' + getTextOfCommand(a)

            dout.next = mem[int(addr)//4]

    return read
