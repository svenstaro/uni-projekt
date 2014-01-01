from myhdl import *

def pseudoram(clk, we, oe, cs, addr, data_in, data_out, depth=128):
    """This is a pseudoram
    """

    mem = [Signal(intbv(0)[8:]) for _ in range(depth)]

    @always(clk.posedge)
    def write():
        if cs and we:
            assert int(addr) < len(mem)

            mem[int(addr)+0].next = data_in[32:24]
            mem[int(addr)+1].next = data_in[24:16]
            mem[int(addr)+2].next = data_in[16: 8]
            mem[int(addr)+3].next = data_in[ 8: 0]


    @always_comb
    def read():
        if cs and oe:
            assert int(addr) < len(mem)

            if __debug__:
                a = bin(mem[int(addr)] << 24 | mem[int(addr)+1] << 16 | mem[int(addr)+2] << 8 | mem[int(addr)+3], width=32)
                print "RAM (" + '0x%02X' % addr + "): " + ' '.join(map(lambda *xs: ''.join(xs), *[iter(a)]*8))

            #data_out.next = mem[int(addr)]
            data_out.next = mem[int(addr)] << 24 | mem[int(addr)+1] << 16 | mem[int(addr)+2] << 8 | mem[int(addr)+3]

    return write, read
