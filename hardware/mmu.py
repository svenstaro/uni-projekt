from myhdl import *

def mmu(clk, en, din, dout, ready, addr, io, enO, enW, csRam, csRom, hit):
    """This unit can be used to abstract the actual memory access. Also we can implement some caching here

        clk   (Ibool) -- The clock
        --- cpu side
        en    (Ibool) -- Enablebit
        din   (I32)   -- input
        dout  (O32)   -- output
        ready (Obool) -- Indicates, that the calculation is performed.
        --- memory side
        addr  (O32)   -- The desired address
        io    (IO32)  -- In-/Output (tristate)
        enO   (Obool) -- Enable output
        enW   (Obool) -- Enable write
        csRam (Obool) -- chip select for ram
        csRom (Obool) -- chip select for rom
        hit   (Ibool) -- If cache is present, is there a hit?!

        To 'communicate' with the unit you have to do the following steps:
          1. enable the mmu with the addr as input
          2. [enable the mmu with value to put in the specific addr (for writing)] [optional]
          3. disable the mmu
          4. wait for the ready bit
          5. get the result
    """

    tState = enum('LISTEN', 'CALC', 'FINISH')
    state = Signal(tState.LST_ADDR)
    waitingtimer = Signal(intbv(0)[4:]) # increase the bitwidth of the timer, if loading takes longer
    with_data = Signal(bool(0))
    in_data = Signal(intbv(0)[32:])

    @always(clk.posedge)
    def write():
        if en:
            if state == tState.LISTEN:
                ready.next = False

                addr.next = din[31:]
                csRam.next = din[31]
                csRom.next = not din[31]
                state.next = tState.CALC
            elif state == tState.CALC:
                with_data.next = True
                in_data.next = din
            else:
                print "Something went wrong!"
        elif state == tState.CALC:
            waitingtimer.next = waitingtimer + 1
            if not with_data:
                #reading from memory
                enO.next = True
                if waitingtimer == 0: # 0 is the number of cycles to wait for the result from cache (which should be significant lower than memory)
                    pass
                elif waitingtimer == 5: # 5 is the number of cycles to wait for the result from memory
                    in_data.next = io
                    state.next = tState.FINISH
            else:
                #writing to memory
                enW.next = True
                io.next = in_data

                if waitingtimer == 2: # 2 is the number of cycles to wait for the result to be written in memory
                    state.next = tState.FINISH

        elif state == tState.FINISH:
            waitingtimer.next = 0
            with_data.next = False
            enO.next = False
            enW.next = False
            ready.next = True
            state.next = tState.LISTEN

    @always_comb
    def read():
        if ready:
            dout.next = in_data


    return write, read
