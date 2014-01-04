from myhdl import *

def registerbank(clk, we, addrx, addry, addrz, xout, yout, zin, amount = 16, bitwidth = 32, protect0=True):
    reg_data = [Signal(intbv(0)[bitwidth:]) for _ in range(amount)]

    @always(clk.posedge)
    def write():
        assert addrx < amount
        assert addry < amount
        assert addrz < amount

        if we and not(protect0 and addrz == 0):
            reg_data[addrz].next = zin[bitwidth:]

    @always_comb
    def read():
        assert addrx < amount
        assert addry < amount
        assert addry < amount

        xout.next = reg_data[addrx]
        yout.next = reg_data[addry]

    return write, read
