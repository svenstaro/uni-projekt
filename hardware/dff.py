from myhdl import *

def dff(clk, d, q):
    """Simple D-Flipflop
    """

    @always(clk.posedge)
    def logic():
        q.next = d

    return logic