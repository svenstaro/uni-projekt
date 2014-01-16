from myhdl import *

def iodevice(clk, enable, dout, din, leds, buttons):
    ledBuffer = Signal(intbv(0)[4:])

    @always(clk.posedge)
    def logic():
        if enable:
            ledBuffer.next = din[4:]

        dout.next = concat(intbv(0)[28:], buttons)
        leds.next = ledBuffer

    return logic
