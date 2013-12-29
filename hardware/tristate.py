from myhdl import *

def tristate(input, enable, res):
    """Tristate which puts the input to the output if enable, None elsewise
    """

    @always_comb
    def logic():
        if enable:
            res.next = input
        else:
            res.next = None

    return logic

