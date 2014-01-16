from math import log
from myhdl import *

def rs232rx(clk, reset, rx, dout, avail, clkFreq=50000000, baudRate=57600):

    timeoutOne  = int(1.0*clkFreq/baudRate)-1
    timeoutHalf = int(1.5*clkFreq/baudRate)-1
    tState = enum('IDLE', 'READ')

    state = Signal(tState.IDLE)
    data = Signal(intbv(0)[8:])
    clkCnt = Signal(modbv(0)[log(timeoutHalf, 2)+1:])
    bitCnt = Signal(modbv(0)[4:])

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if clkCnt > 0:
            clkCnt.next = clkCnt - 1
        else:
            if state == tState.IDLE:
                if not rx:
                    avail.next = False
                    data.next = 0
                    bitCnt.next = 8
                    clkCnt.next = timeoutHalf
                    state.next = tState.READ
            elif state == tState.READ:
                clkCnt.next = timeoutOne
                if bitCnt > 0:
                    data.next = data | (rx << (8 - bitCnt))
                    bitCnt.next = bitCnt - 1
                else:
                    dout.next = data
                    avail.next = True
                    state.next = tState.IDLE

    return logic
