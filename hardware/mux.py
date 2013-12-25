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
        if not s1:
            if not s0:
                out.next = i00
            else:
                out.next = i01
        else:
            if not s0:
                out.next = i10
            else:
                out.next = i11

    return logic

def mux21(s, A, B, out):
    """Simple 2:1 multiplexer

    All parameters are Signals as usual

    s0  (Ibool) -- selector
    A   (I)     -- first input
    B   (I)     -- second input
    out (O)     -- output

    the output is defined by the selector and the specific output.
    all Is and O must have the same bitlength
    """
    @always_comb
    def logic():
        if not s:
            out.next = A
        else:
            out.next = B

    return logic

