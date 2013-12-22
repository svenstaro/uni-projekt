from myhdl import *

def tristate(input, enable, odriver):
    """Tristate which puts the input to the output if enable, None elsewise
    """

    @always_comb
    def logic():
        if enable:
            odriver.next = intbv(input.val)
        else:
            odriver.next = None

    return logic

