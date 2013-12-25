from myhdl import *

def mux21(s, A, B, out):

    @always_comb
    def logic():
        if not s:
            out.next = A
        else:
            out.next = B

    return logic
