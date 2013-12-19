from myhdl import *

def programcounter(clk, reset, enabled, a, b, c, d, select1, select2, out):
    """Represents the programcounter (PC)

    clk              -- The clock
    reset            -- A reset input
    enabled          -- enabled input
    a, b, c, d       -- data input
    select1, select2 -- mux selector
    out              -- data out

    s2 s1 out
    --+--+---
     0| 0| a
    --+--+---
     0| 1| b
    --+--+---
     1| 0| c
    --+--+---
     1| 1| d
    """

    data = Signal(intbv(0)[16:])

    @always_comb(clk.posedge, reset)
    def logic():
        if enabled:
            if   not s2 and not s1:
                data.next = a
            elif not s2 and     s1:
                data.next = b
            elif     s2 and not s1:
                data.next = c
            else:
                data.next = d

        out.next = data

    return logic
