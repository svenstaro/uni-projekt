from myhdl import *

def register(clk, reset, we, data_in, data_out, bitwidth=32):
    data = Signal(intbv(0)[bitwidth:])

    @always_seq(clk.posedge, reset)
    def logic():
        if we:
            data.next = data_in
        data_out.next = data

    return logic

