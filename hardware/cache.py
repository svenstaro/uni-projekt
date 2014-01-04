# -*- coding: utf-8 -*-

from myhdl import *
from hardware.registerbank import registerbank


def cache(clk, addr, io, enO, enW, csRam, csRom, hit, ready):
    """Implements some kind of caching

    clk   (Ibool) -- the clock
    addr  (I31)   -- The destination addr
    io    (IO32)  -- In-/Output (tristate)
    enO   (Ibool) -- Enable output
    enW   (Ibool) -- enable write
    csRam (Ibool) -- chip select for ram
    csRom (Ibool) -- chip select for rom
    hit   (Obool) -- cache hit?!
    ready (Ibool) -- readybit from mmu

    Current cachesize is 128
    """

    #TODO implement variable cachesize

    def myHash(a):
        return (csRam ^ csRom ^ a[31:28] ^ a[28:21] ^ a[21:14] ^ a[14:7] ^ a[7:0])

    tState = enum('IDLE', 'SEARCH', 'INSERT', 'DELETE', 'FINISH')
    state = Signal(tState.IDLE)
    iodriver = io.driver()

    data_we = Signal(bool(0))
    data_addr = Signal(intbv(0)[7:])
    data_in = Signal(intbv(0)[65:])
    #1 clean bit (0 → dirty, 1 → clean) + 1 csbit (0→Rom, 1→Ram) + 31bit addr + 32bit data
    data_out = Signal(intbv(0)[65:])

    data = registerbank(clk, data_we, data_addr, Signal(intbv(0)[1:]), data_addr,
                        data_out, Signal(intbv(0)[65:]), data_in, amount=128, bitwidth=65, protect0=False)

    @always(clk.posedge)
    def logic():
        if state == tState.IDLE:
            data_addr.next = myHash(addr)
            if enW:
                state.next = tState.DELETE
            elif enO:
                state.next = tState.SEARCH
            else:
                state.next = tState.IDLE
        elif state == tState.DELETE:
            if data_out[63] == csRam and data_out[63:32] == addr:  # if cached addr is same as current one
                data_in.next = data_out & ~(1 << 64)  # clear clean bit
                data_we.next = True
            state.next = tState.FINISH
        elif state == tState.SEARCH:
            #check if clean flag is set, we inspect the right memory and the addr is also the same
            if data_out[64] and data_out[63] == csRam and data_out[63:32] == addr:
                hit.next = True
                state.next = tState.FINISH
            else:
                hit.next = False
                state.next = tState.INSERT
        elif state == tState.INSERT:
            if ready:  # wait until the ready bit is set (by the mmu)
                data_in.next = True << 64 | csRam << 63 | addr << 32 | io
                data_we.next = True
                state.next = tState.FINISH
        elif state == tState.FINISH:
            if hit:
                iodriver.next = data_out[32:0]
            data_we.next = False
            if ready:  # wait for the ready bit of the mmu
                state.next = tState.IDLE
        if not enO:
            iodriver.next = None
            hit.next = False

    return data, logic
