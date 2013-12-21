from myhdl import *

def addrdecoder(addr, enRam, enRom, bitwidth=32):
    """This is the addressdecoder.
        It is responsible for turning on/off the specific memory (ram/rom).

    addr (Ibw)      -- Input addr
    enRam (Obool)   -- Enablebit for Ram, true if MSB of addr is set
    enRom (Obool)   -- Enablebit for Rom, true if MSB of addr is not set
    """

    @always_comb
    def logic():
        enRam.next = addr[bitwidth-1]
        enRom.next = not addr[bitwidth-1]

    return logic
