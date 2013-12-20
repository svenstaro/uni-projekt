from myhdl import *

def mux41(s1, s0, i00, i01, i10, i11, out):
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
