from myhdl import *

def andd(A, B, R):

    @always_comb
    def logic():
        R.next = A & B

    return logic
