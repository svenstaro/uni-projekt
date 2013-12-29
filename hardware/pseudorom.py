from myhdl import *

def pseudorom(oe, cs, addr, dout, mem):
    """This is a pseudorom
    """

    @always_comb
    def read():
        if cs and oe:
            assert int(addr)//4 < len(mem)
            
            dout.next = mem[int(addr)//4]

    return read
