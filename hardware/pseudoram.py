from myhdl import *

def pseudoram(clk, we, oe, cs, addr, data_in, data_out, depth=128):
    """This is a pseudoram
    """

    mem = [Signal(intbv(0)[32:]) for _ in range(depth)]

    @always(clk.posedge)
    def write():
        if cs and we:
            assert int(addr) < len(mem)

            mem[int(addr)].next = data_in

    @always_comb
    def read():
        if cs and oe:
            assert int(addr) < len(mem)

            data_out.next = mem[int(addr)]
        elif not cs:
            data_out.next = None

    return write, read
