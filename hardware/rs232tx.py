from math import log
from myhdl import *

def rs232tx(clk, reset, readybit, start, din, tx, clkFreq=50000000, baudRate=57600):

    timeoutOne  = int(1.0*clkFreq/baudRate)-1
    timeoutHalf = int(1.5*clkFreq/baudRate)-1
    tState = enum('IDLE', 'SEND')

    state = Signal(tState.IDLE)
    data = Signal(intbv(0)[32:])
    clkCnt = Signal(modbv(0)[log(timeoutHalf, 2):])
    bitCnt = Signal(modbv(0)[4:])

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if clkCnt > 0:
            clkCnt.next = clkCnt - 1
        else:
            tx.next = True
            if state == tState.IDLE:
                if start:
                    data.next = din
                    clkCnt.next = timeoutOne
                    bitCnt.next = 8
                    tx.next = False
                    state.next = tState.SEND
            elif state == tState.SEND:
                if bitCnt > 0:
                    tx.next = data[8-bitCnt]
                    bitCnt.next = bitCnt - 1
                    clkCnt.next = timeoutOne
                else:
                    tx.next = True
                    readybit.next = True
                    clkCnt.next = timeoutHalf
                    state.next = tState.IDLE

    return logic
