from myhdl import *

def adder(A, B, S):

    @always_comb
    def logic():
        S = A ^ B

    return logic

