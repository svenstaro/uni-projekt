from myhdl import *

def registerbank(clk, we, channel, data_in, data_out, amount = 16, bitwidth = 32):
    reg_data = [Signal(intbv(0)[bitwidth:]) for _ in range(1, amount)]

    @always(clk.posedge)
    def write():
        assert channel < amount

        if channel != 0: #zero register is always zero!
            if we:
                reg_data[channel-1].next = data_in

            data_out.next = reg_data[channel-1]

    @always_comb
    def read():
        assert channel < amount

        if channel == 0:
            data_out.next = 0
        else:
            data_out.next = reg_data[channel-1]

    return write, read

