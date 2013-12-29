from myhdl import *

def registerr(clk, reset, we, din, dout, bitwidth=32):
    data = Signal(intbv(0)[bitwidth:])

    @always_seq(clk.posedge, reset)
    def write():
        if we:
            data.next = din

    @always_comb
    def read():
        dout.next = data

    return write, read
