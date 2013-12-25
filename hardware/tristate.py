from myhdl import *

def tristate(input, enable, out):
    """Tristate which puts the input to the output if enable, None elsewise
    """

    o = out.driver()

    @always_comb
    def logic():
        o.next = input if enable else None

    return logic

