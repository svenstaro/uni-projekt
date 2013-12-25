from myhdl import *

def pseudoram(clk, we, oe, cs, addr, data_in, data_out, depth=128):
    """This is a pseudoram
    """

    out = data_out.driver()

    mem = [Signal(intbv(0)[32:]) for _ in range(depth)]

    @always(clk.posedge)
    def write():
        assert addr < len(mem)
        if cs and we:
            mem[int(addr)].next = data_in

    @always_comb
    def read():
        assert addr < len(mem)

        if cs and oe:
            out.next = mem[int(addr)]

    return write, read
