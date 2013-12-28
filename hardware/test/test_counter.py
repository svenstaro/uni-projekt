from unittest import TestCase
from myhdl import *
from counter import *

class DutClass():
    """Wrapper around DUT"""
    def __init__(self):
        self.clk = Signal(bool(0))
        self.reset = ResetSignal(0, 1, True)
        self.enable = Signal(bool(0))
        self.dout = Signal(intbv(0)[32:])

    def Gens(self, trace = False):
        self.args = [self.clk, self.reset, self.enable, self.dout]
        
        return traceSignals(counter, *self.args) if trace else counter(*self.args)

def genSim(verifyMethod, cl=DutClass, clkfreq=1, trace=False):
    """ Generates a Simulation Object """

    dut_cl = cl()

    @always(delay(clkfreq))
    def clkGen():
        dut_cl.clk.next = not dut_cl.clk

    @instance
    def stimulus():
        dut_cl.reset.next = True
        yield delay(4*clkfreq)
        dut_cl.reset.next = False

        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    dut = dut_cl.Gens(trace=trace)
    return Simulation(dut, clkGen, stimulus)


class CounterTest(TestCase):
    def testCounting(self):
        def verify(cl, dut):
            cl.enable.next = True
            for i in range(128):
                yield cl.clk.posedge
                self.assertEquals(i, cl.dout)

        genSim(verify).run()

# vim: set ft=python:
