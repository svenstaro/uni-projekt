from unittest import TestCase
from myhdl import *
from registerbank import *

class DutClass():
    """Wrapper around DUT"""
    def __init__(self, clkfreq=1, bitwidth=8, numChannel=5):
        self.clk = Signal(bool(0))
        self.reset = ResetSignal(0,1,True)
        self.we = Signal(bool(0))
        self.inn = Signal(intbv(0)[bitwidth:])
        self.out = Signal(intbv(0)[bitwidth:])
        self.channel = Signal(intbv(0,0,numChannel))
        self.clkfreq = clkfreq
        self.bitwidth = bitwidth
        self.numChannel = numChannel

    def Gens(self, traceSignal = False):
        if traceSignal:
            dut = traceSignals(registerbank,self.clk,
                               self.reset,self.we,self.channel,
                               self.inn,self.out,
                               amount = self.numChannel,
                               bitwidth=self.bitwidth)
        else:
            dut = registerbank(self.clk,
                               self.reset,self.we,self.channel,
                               self.inn,self.out,
                               amount = self.numChannel,
                               bitwidth=self.bitwidth)

        return dut
def genSim(verifyMethod, cl=DutClass(), clkfreq=1, traceSignal=False):
    
    @always(delay(clkfreq))
    def clkGen():
        cl.clk.next = not cl.clk

    @instance
    def stimulus():
        cl.reset.next = True
        yield delay(2)
        cl.reset.next = False

        yield verifyMethod(cl, dut)
        raise StopSimulation

    dut = cl.Gens(traceSignal=traceSignal)
    return Simulation(dut, clkGen, stimulus)


class RegisterbankTest(TestCase):
       def testZeroRegister(self):
        """Check if register 0 is always 0"""

        def verify(cl, dut):
            cl.we.next = 1
            cl.inn.next = intbv(1)
            yield cl.clk.negedge
            self.assertEquals(0, cl.out)

            cl.inn.next = intbv(30)
            yield cl.clk.negedge
            self.assertEquals(0, cl.out)

            cl.we.next = 0
            cl.inn.next = intbv(22)
            yield cl.clk.negedge
            self.assertEquals(0, cl.out)

        genSim(verify).run()




# vim: set ft=python:

