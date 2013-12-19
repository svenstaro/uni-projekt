from myhdl import *

def registerbank(clk, we, addrx, addry, addrz, xout, yout, zin, amount = 16, bitwidth = 32):
    reg_data = [Signal(intbv(0)[bitwidth:]) for _ in range(1, amount)]

    @always(clk.posedge)
    def logic():
        assert addrx < amount
        assert addry < amount
        assert addrz < amount

        xout.next = 0 if addrx == 0 else reg_data[addrx-1]
        yout.next = 0 if addry == 0 else reg_data[addry-1]

        if we and addrz != 0:
            reg_data[addrz-1].next = zin[bitwidth:]

    return logic
