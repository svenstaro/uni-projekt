from myhdl import *

def tristate(input, enable, res):
    """Tristate which puts the input to the output if enable, None elsewise
    """

    o = res.driver()

    @always_comb
    def logic():
        o.next = input if enable else None

    return logic

