from myhdl import *

def pseudoram(clk, we, oe, cs, addr, data_in, data_out, mem=[Signal(intbv(0)[32:]) for _ in range(128)]):
    """This is a pseudoram
    """

    @always(clk.posegde)
    def write():
        assert addr < len(mem)
        if cs and we:
            mem[addr].next = data_in

    @always_comb
    def read():
        assert addr < len(mem)

        if cs and oe:
            data_out.next = mem[addr]

    return write, read
