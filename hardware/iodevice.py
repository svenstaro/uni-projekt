from myhdl import *


def iodevice(clk, reset, enable, dout, din, leds, buttons):
    ledBuffer = Signal(intbv(0)[4:])

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if enable:
            ledBuffer.next = din[4:]

        dout.next = ~buttons
        leds.next = ~ledBuffer

    return logic
