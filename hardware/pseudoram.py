from myhdl import *

def pram(clk, we, addr, data_in, data_out, depth=128):
    
    mem = [Signal(intbv(0)[32:]) for _ in range(128)]

    @always(clk.posegde)
    def write():
        if we:
            mem[addr].next = data_in

    @always_comb
    def read():
        data_out.next = mem[addr]

    return write, read

