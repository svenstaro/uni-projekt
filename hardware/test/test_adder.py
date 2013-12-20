from unittest import TestCase
from myhdl import *
from adder import *

class DutClass():
    """Wrapper around DUT"""
    def __init__(self,bitwidth=16):
        self.clk = Signal(bool(0))

        self.a, self.b, self.s = [Signal(modbv(0)[bitwidth:]) for _ in range(3)]

    def Gens(self, trace = False):
        args = [self.a, self.b, self.s]

        return traceSignals(adder, *args) if trace else adder(*args)

def genSim(verifyMethod, cl=DutClass, clkfreq=1, trace=False):
    """ Generates a Simulation Object """

    dut_cl = cl()

    @always(delay(clkfreq))
    def clkGen():
        dut_cl.clk.next = not dut_cl.clk

    @instance
    def stimulus():

        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    dut = dut_cl.Gens(trace=trace)
    return Simulation(dut, clkGen, stimulus)


class AdderTest(TestCase):
    def testaddition(self):
        def verify(cl, dut):
            cl.a.next = 3
            cl.b.next = 5
            yield cl.clk.posedge

            self.assertEquals(8, cl.s)

        genSim(verify).run()

# vim: set ft=python:
