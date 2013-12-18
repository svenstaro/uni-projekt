from myhdl import *

def pseudoram(clk, we, addr, data_in, data_out, depth=128):
    mem = [Signal(intbv(0)[32:]) for _ in range(128)]

    @always(clk.posegde)
    def write():
        assert addr >= len(mem)

        if we:
            mem[addr].next = data_in

    @always_comb
    def read():
        assert addr < len(mem)

        data_out.next = mem[addr]

    return write, read

