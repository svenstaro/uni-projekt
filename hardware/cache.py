from myhdl import *

def cache(clk, addr, io, enO, enW, csRam, csRom, hit, ready):
    """Implements some kind of caching

    clk   (Ibool) -- the clock
    addr  (I32)   -- The destination addr
    io    (IO32)  -- In-/Output (tristate)
    enO   (Ibool) -- Enable output
    enW   (Ibool) -- enable write
    csRam (Ibool) -- chip select for ram
    csRom (Ibool) -- chip select for rom
    hit   (Obool) -- cache hit?!
    ready (Ibool) -- readybit from mmu
    """

    tState = enum('IDLE', 'SEARCH', 'FINISH')
    state = tState.IDLE
    in_data = Signal(intbv(0)[32:])
    iodriver = io.driver()

    @always(clk.posedge)
    def write():
        if enO:
            pass

    @always_comb
    def read():
        if hit:
            iodriver.next = in_data

    return write, read
