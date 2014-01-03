from myhdl import *
from math import log

def pseudoram(clk, we, oe, cs, addr, din, dout, depth=128, readdelay=1, writedelay=1):
    """This is a pseudoram with a specific delay
    """

    mem = [Signal(intbv(0)[8:]) for _ in range(depth)]
    r = Signal(intbv(1)[int(log(readdelay, 2)+1):])
    w = Signal(intbv(1)[int(log(writedelay, 2)+1):])

    if __debug__:
        geread = Signal(False)
        gewead = Signal(False)

    @always(clk.posedge)
    def write():
        if cs and we:
            assert int(addr) < len(mem)

            if w < writedelay:
                w.next = w + 1
            else:
                if __debug__:
                    gewead.next = True
                    if not gewead:
                        a = bin(din, width=32)
                        print "RAMw(" + '0x%02X' % addr + "): " + ' '.join(map(lambda *xs: ''.join(xs), *[iter(a)]*8)) + ' | ' + '0x%X %d' % (din,din)

                mem[int(addr)+0].next = din[32:24]
                mem[int(addr)+1].next = din[24:16]
                mem[int(addr)+2].next = din[16: 8]
                mem[int(addr)+3].next = din[ 8: 0]
        else:
            if __debug__:
                gewead.next = False
            w.next = 1


    @always(clk.posedge, oe, cs)
    def read():
        dout.next = None

        if cs and oe:
            assert int(addr) < len(mem)

            if r < readdelay:
                r.next = r + 1
            elif r == readdelay:
                if __debug__:
                    geread.next = True
                    if not geread:
                        d = mem[int(addr)] << 24 | mem[int(addr)+1] << 16 | mem[int(addr)+2] << 8 | mem[int(addr)+3]
                        a = bin(d, width=32)
                        print "RAMr(" + '0x%02X' % addr + "): " + ' '.join(map(lambda *xs: ''.join(xs), *[iter(a)]*8)) + ' | ' + '0x%X %d' % (d,d)

                dout.next = mem[int(addr)] << 24 | mem[int(addr)+1] << 16 | mem[int(addr)+2] << 8 | mem[int(addr)+3]
        else:
            if __debug__:
                geread.next = False
            dout.next = None
            r.next = 1

    return write, read
