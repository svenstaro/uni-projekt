from myhdl import *
from math import log
from assembler import getTextOfCommand

def pseudorom(clk, oe, cs, addr, dout, mem, readdelay=1):
    """This is a pseudorom with delay
    """

    r = Signal(intbv(1)[int(log(readdelay, 2)+1):])

    if __debug__:
        geread = Signal(False)

    @always(clk.posedge, cs, oe)
    def read():
        dout.next = None

        if cs and oe:
            assert int(addr)//4 < len(mem)

            if r < readdelay and clk: #clk is high
                r.next = r + 1
            elif r == readdelay:
                if __debug__:
                    geread.next = True
                    if not geread:
                        a = bin(mem[int(addr)//4], width=32)
                        print "ROM (" + '0x%02X' % addr + "): " + ' '.join(map(lambda *xs: ''.join(xs), *[iter(a)]*8)) + ' | ' + str(getTextOfCommand(a))

                dout.next = mem[int(addr)//4]
        else:
            if __debug__:
                geread.next = False

            dout.next = None
            r.next = 1


    return read
