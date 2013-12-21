from unittest import TestCase
from myhdl import *
from addrdecoder import *

class DutClass():
    """Wrapper around DUT"""
    def __init__(self):
        self.addr = Signal(intbv(0)[8:])
        self.enRam, self.enRom = [Signal(bool(0)) for _ in range(2)]

    def Gens(self, trace = False):
        args = [self.addr,self.enRam,self.enRom,8]

        return traceSignals(addrdecoder, *args) if trace else addrdecoder(*args)

def genSim(verifyMethod, cl=DutClass, clkfreq=1, trace=False):
    """ Generates a Simulation Object """

    dut_cl = cl()

    @instance
    def stimulus():
        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    dut = dut_cl.Gens(trace=trace)
    return Simulation(dut, stimulus)


class AddrDecoderTest(TestCase):
    def testDecoding(self):
        """Checks if decoding works correctly"""
        def verify(cl, dut):
            cl.addr.next = 0b01111111
            yield delay(1)
            self.assertEquals(0, cl.enRam)
            self.assertEquals(1, cl.enRom)

            cl.addr.next = 0b10000000
            yield delay(1)
            self.assertEquals(1, cl.enRam)
            self.assertEquals(0, cl.enRom)

        genSim(verify).run()

# vim: set ft=python:
