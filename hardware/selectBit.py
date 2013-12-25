from myhdl import *

def selectBit(A, R, bit=0):

    @always_comb
    def logic():
        assert bit < len(A)

        R.next = a[bit]

    return logic
