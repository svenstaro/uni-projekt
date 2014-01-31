from myhdl import *


def mmu(clk, reset,
        en, din, dout, ready,
        addr, ioIn, ioOut, enO, enW, csRam, csRom, hit):
    """This unit can be used to abstract the actual memory access. Also we can implement some caching here

        clk   (Ibool) -- The clock
        reset (Ireset)-- The reset
        --- cpu side
        en    (Ibool) -- Enablebit
        din   (I32)   -- input
        dout  (O32)   -- output
        ready (Obool) -- Indicates, that the calculation is performed.
        --- memory side
        addr  (O16)   -- The desired address
        ioIn  (I32)   -- Input
        ioOut (O32)   -- Output
        enO   (Obool) -- Enable output
        enW   (Obool) -- Enable write
        csRam (Obool) -- chip select for ram
        csRom (Obool) -- chip select for rom
        hit   (Ibool) -- Is there a cache hit?!

        To 'communicate' with the unit you have to do the following steps:
          1. enable the mmu with the addr as input - clk
          2. [enable the mmu with value to put in the specific addr (for writing)] [optional] - clk
          3. disable the mmu - clk
          4. wait at least one clk
          5. wait for the ready bit
          6. get the result

        You have to wait at least 1 cycle for initializing all the things before you can wait for the ready signal!
    """

    tState = enum('LISTEN', 'CALC', 'FINISH')
    state = Signal(tState.LISTEN)
    waitingtimer = Signal(intbv(0)[8:])  # increase the bitwidth of the timer, if loading takes longer
    with_data = Signal(bool(0))
    in_data = Signal(intbv(0)[32:])

    @always_seq(clk.posedge, reset=reset)
    def write():
        if ready:
            dout.next = in_data

        if en:
            if state == tState.LISTEN:
                ready.next = False
                addr.next = din[16:]
                csRam.next = din[31]
                csRom.next = not din[31]
                state.next = tState.CALC
            elif state == tState.CALC:
                assert bool(csRam)  # make sure the high bit is set

                csRam.next = True
                csRom.next = False
                with_data.next = True
                in_data.next = din
            else:
                print "Something went wrong! (Did you read the protocoll?)"
        elif state == tState.CALC:
            assert not(enO and enW)  # they are not allowed to be true at once

            waitingtimer.next = waitingtimer + 1
            if not with_data:
                #reading from memory
                enO.next = True
                if waitingtimer == 4 and hit:  # cache hit?
                        in_data.next = ioIn
                        state.next = tState.FINISH
                elif waitingtimer == 1:  # 10 is the number of cycles to wait for the result from memory
                    in_data.next = ioIn
                    state.next = tState.FINISH
            else:
                #writing to memory
                enW.next = True
                ioOut.next = in_data

                if waitingtimer == 1:  # 15 is the number of cycles to wait for the result to be written in memory
                    state.next = tState.FINISH
        elif state == tState.FINISH:
            waitingtimer.next = 0
            with_data.next = False
            enO.next = False
            enW.next = False
            ready.next = True
            state.next = tState.LISTEN

    return write
