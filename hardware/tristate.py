from myhdl import *

def tristate(input, enable, out):
    """Tristate which puts the input to the output if enable, None elsewise
    """

    @always_comb
    def logic():
        out.next = input if enable else None

    return logic

