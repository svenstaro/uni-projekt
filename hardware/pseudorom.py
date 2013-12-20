from myhdl import *

def pseudorom(clk, we, addr, data_out, mem=[]):

    @always_comb
    def read():
        assert addr < len(mem)

        data_out.next = mem[addr]

    return read

