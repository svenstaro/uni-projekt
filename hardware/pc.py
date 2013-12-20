from myhdl import *
from register import *
from mux41 import *

def programcounter(clk, reset, enabled, i00, i01, i10, i11, s1, s0, out, width=32):
    """Represents the programcounter (PC)

    All parameters are Signals as usual

    clk (Ibool)     -- The clock
    reset (Ireset)  -- A reset input
    enabled (Ibool) -- enabled input
    i00,i01,i10,i11 -- data input
    s1, s0          -- mux selector
    out             -- data out

    """

    outin = Signal(intbv(0)[width:])
    mux = mux41(s1, s0, i00, i01, i10, i11, outin)
    reg = register(clk, reset, enabled, outin, out, bitwidth=width)

    return mux, reg
