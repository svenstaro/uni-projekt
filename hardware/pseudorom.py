from myhdl import *

def pseudorom(oe, cs, addr, data_out, mem):
    """This is a pseudorom
    """

    out = data_out.driver()

    @always_comb
    def read():
        assert addr < len(mem)

        if cs and oe:
            out.next = mem[int(addr)]

    return read
