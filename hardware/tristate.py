from myhdl import *

def tristate(input, enable, odriver):
    """Tristate which puts the input to the output if enable, None elsewise
    """

    @always_comb
    def logic():
        odriver.next = input if enable else None

    return logic

