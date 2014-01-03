from myhdl import *
from math import log

def pseudoram(clk, we, oe, cs, addr, din, dout, depth=128, readdelay=1, writedelay=1):
    """This is a pseudoram with a specific delay
    """

    mem = [Signal(intbv(0)[8:]) for _ in range(depth)]
    r = Signal(intbv(1)[int(log(readdelay, 2)+1):])
    w = Signal(intbv(1)[int(log(writedelay, 2)+1):])

    @always(clk.posedge)
    def write():
        if cs and we:
            assert int(addr) < len(mem)

            if w < writedelay:
                w.next = w + 1
            else:
                if __debug__:
                    a = bin(din, width=32)
                    print "RAMw(" + '0x%02X' % addr + "): " + ' '.join(map(lambda *xs: ''.join(xs), *[iter(a)]*8)) + ' | ' + '0x%X %d' % (din,din)

                mem[int(addr)+0].next = din[32:24]
                mem[int(addr)+1].next = din[24:16]
                mem[int(addr)+2].next = din[16: 8]
                mem[int(addr)+3].next = din[ 8: 0]
        else:
            w.next = 1


    @always(clk.posedge, oe, cs, addr)
    def read():
        dout.next = None

        if cs and oe:
            assert int(addr) < len(mem)

            if r < readdelay and clk: #clk is high
                r.next = r + 1
            elif r == readdelay:
                if __debug__:
                    a = bin(mem[int(addr)] << 24 | mem[int(addr)+1] << 16 | mem[int(addr)+2] << 8 | mem[int(addr)+3], width=32)
                    print "RAMr(" + '0x%02X' % addr + "): " + ' '.join(map(lambda *xs: ''.join(xs), *[iter(a)]*8))

                dout.next = mem[int(addr)] << 24 | mem[int(addr)+1] << 16 | mem[int(addr)+2] << 8 | mem[int(addr)+3]
        else:
            dout.next = None
            r.next = 1

    return write, read
