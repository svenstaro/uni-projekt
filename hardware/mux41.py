from myhdl import *

def mux41(s1, s0, i00, i01, i10, i11, out):
    """Simple 4:1 multiplexer

    All parameters are Signals as usual

    s1 (Ibool)  -- selector high
    s0 (Ibool)  -- selector low
    i00 (I)     -- first input
    i01 (I)     -- second input
    i10 (I)     -- third input
    i11 (I)     -- fourth input
    out (O)     -- output

    the output is defined by the selector and the specific output.
    all Is and O must have the same bitlength
    """
    @always_comb
    def logic():
        if   not s1 and not s0:
            out.next = i00
        elif not s1 and     s0:
            out.next = i01
        elif     s1 and not s0:
            out.next = i10
        else:
            out.next = i11

    return logic
