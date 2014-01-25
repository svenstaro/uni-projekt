from myhdl import *
from math import log
from assembler import getTextOfCommand


def pseudorom(oe, addr, dout, mem):
    """This is a pseudorom with delay
    """

    o = dout.driver()

    @always_comb
    def read():
        o.next = None

        if oe:
            assert int(addr) <= len(mem) - 4

            if __debug__:
                cont = mem[addr] << 24 | mem[addr+1] << 16 | mem[addr+2] << 8 | mem[addr+3]
                a = bin(cont, width=32)
                print "ROM (" + '0x%02X' % addr + "): " + ' '.join(map(lambda *xs: ''.join(xs), *[iter(a)]*8)) + ' | ' + str(getTextOfCommand(a))


            imm1 = mem[addr+0]
            imm2 = mem[addr+1]
            imm3 = mem[addr+2]
            imm4 = mem[addr+3]

            o.next = imm1 << 24 | imm2 << 16 | imm3 << 8 | imm4

    return read
