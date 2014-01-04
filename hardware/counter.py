from myhdl import *
from adder import *
from register import *

def counter(clk, reset, enable, dout, bitwidth=32):

    data = Signal(modbv(0)[bitwidth:])

    @always_seq(clk.posedge, reset)
    def write():
        if enable:
            data.next = data + 1

    @always_comb
    def read():
        dout.next = data

    return write, read
