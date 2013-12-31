from myhdl import *

def bitrange(input, result, start=0, end=1):

    @always_comb
    def logic():
        result.next = input[end:start]

    return logic
