from myhdl import *

def pseudoram(clk, we, oe, cs, addr, din, dout, depth=128):
    """This is a pseudoram
    """

    mem = [Signal(intbv(0)[8:]) for _ in range(depth)]

    @always(clk.posedge)
    def write():
        if cs and we:
            assert int(addr) < len(mem)

            mem[int(addr)+0].next = din[32:24]
            mem[int(addr)+1].next = din[24:16]
            mem[int(addr)+2].next = din[16: 8]
            mem[int(addr)+3].next = din[ 8: 0]


    @always_comb
    def read():
        dout.next = None

        if cs and oe:
            assert int(addr) < len(mem)

            if __debug__:
                a = bin(mem[int(addr)] << 24 | mem[int(addr)+1] << 16 | mem[int(addr)+2] << 8 | mem[int(addr)+3], width=32)
                print "RAM (" + '0x%02X' % addr + "): " + ' '.join(map(lambda *xs: ''.join(xs), *[iter(a)]*8))

            #dout.next = mem[int(addr)]
            dout.next = mem[int(addr)] << 24 | mem[int(addr)+1] << 16 | mem[int(addr)+2] << 8 | mem[int(addr)+3]

    return write, read
