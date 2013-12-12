from myhdl import *

def register(clk, reset, we, data_in, data_out):
    data = Signal(intbv(0)[16:])

    @always_seq(clk.posedge, reset)
    def logic():
        if we:
            data.next = data_in
        data_out.next = data

    return logic

