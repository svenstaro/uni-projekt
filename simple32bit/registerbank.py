from myhdl import *

def registerbank(clk, reset, we, channel, data_in, data_out, amount = 16, bitwidth = 32):
    data = [intbv(0)[bitwidth:] for _ in range(1, amount)]

    @always_seq(clk.posedge, reset=reset)
    def logic():
        assert channel < amount

        if channel == 0: #zero register is always zero!
            data_out.next = 0
        else:
            if we:
                data[channel-1] = intbv(data_in.val) #make sure to create a new object! elsewise this would be a reference, which is not, what you want!
            data_out.next = data[channel-1]

    return logic

