from myhdl import *

def pseudorom(clk, we, addr, data_out, mem=[]):
    intmem = mem

    @always_comb
    def read():
        assert addr < len(intmem)

        data_out.next = intmem[addr]

    return read

