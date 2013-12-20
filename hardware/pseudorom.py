from myhdl import *

def pseudorom(clk, we, oe, addr, data_in, data_out, mem=[]):
    """This is a pseudorom
    """
    @always_comb
    def read():
        assert addr < len(mem)

        if oe:
            data_out.next = mem[addr]

    return read
