from myhdl import *

def registerbank(clk, reset, we, channel, data_in, data_out, amount = 16, bitwidth = 32):
    data = [intbv(0)[bitwidth:] for _ in range(1, amount)]

    @always_seq(clk.posedge, reset=reset)
    def logic():
        assert channel < amount

        if channel == 0:
            data_out.next = 0
        else:
            if we:
                data[channel-1] = intbv(data_in.val)
            data_out.next = data[channel-1]

    return logic

