from myhdl import *
from adder import *
from register import *

def counter(clk, reset, enable, data_out, bitwidth=32):

    sig = Signal(intbv(1)[bitwidth:])

    add = adder(Signal(intbv(1)[bitwidth:]), data_out, sig)
    data = registerr(clk, reset, enable, sig, data_out)

    return data, add
