from myhdl import *

def pseudorom(oe, cs, addr, data_out, mem):
    """This is a pseudorom
    """

    @always_comb
    def read():
        if cs and oe:
            assert addr < len(mem)

            data_out.next = mem[int(addr)]

    return read
