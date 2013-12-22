from myhdl import *

def tristate(input, enable, output):
    """Tristate which puts the input to the output if enable, None elsewise
    """

    o = output.driver()

    @always_comb
    def logic():
        if enable:
            o.next = intbv(input.val)
        else:
            o.next = None

    return logic

