from myhdl import *

def registerbank(clk, reset, we, channel, data_in, data_out, amount = 16, bitwidth = 32):
    reg_data = [Signal(intbv(0)[bitwidth:]) for _ in range(1, amount)]

    @always_seq(clk.posedge, reset=reset)
    def logic():
        assert channel < amount

        if channel == 0: #zero register is always zero!
            data_out.next = 0
        else:
            if we:
                reg_data[channel-1].next = data_in

            data_out.next = reg_data[channel-1]

    return logic

