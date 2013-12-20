from myhdl import *

def register(clk, reset, we, data_in, data_out, bitwidth=32):
    data = Signal(intbv(0)[bitwidth:])

    @always_seq(clk.posedge, reset)
    def write():
        if we:
            data.next = data_in

    @always_comb
    def read():
        data_out.next = data

    return write, read

