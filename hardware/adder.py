from myhdl import *

def adder(A, B, S):
    """Simple adder without carry or antyhing

    All parameters are Signals as usual

    A (I)   -- First input
    B (I)   -- Second input
    S (O)   -- Result A+B

    """

    @always_comb
    def logic():
        S.next = A + B

    return logic
