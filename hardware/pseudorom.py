from myhdl import *

def pseudorom(oe, cs, addr, data_out, mem):
    """This is a pseudorom
    """

    @always_comb
    def read():
        assert addr < len(mem)

        if cs and oe:
            data_out.next = mem[int(addr)]

    return read
