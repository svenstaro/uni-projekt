from unittest import TestCase
from myhdl import *
from pc import *
from adder import *

class DutClass():
    """Wrapper around DUT"""
    def __init__(self, bitwidth=8):
        self.clk = Signal(bool(0))
        self.reset = ResetSignal(0, 1, True)

        self.enabled, self.s1, self.s0 = [Signal(bool(0)) for _ in range(3)]
        self.i10, self.i11, self.out = [Signal(intbv(0)[bitwidth:]) for _ in range(3)]

        self.add = adder(self.out, Signal(intbv(2)[bitwidth:]), self.i10)
        self.bitwidth = bitwidth

    def Gens(self, trace = False):
        args = [self.clk, self.reset, self.enabled,
                Signal(intbv(0)[self.bitwidth:]), Signal(intbv(1)[self.bitwidth:]),
                self.i10, self.i11, self.s1, self.s0, self.out,8]

        """It's not connect like this:
        00: always 0
        01: always 1
        10: self.out + 2
        11: self.i11"""

        return traceSignals(programcounter, *args) if trace else programcounter(*args)

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
    return Simulation(dut, clkGen, dut_cl.add, stimulus)


class TestPc(TestCase):
    def testCounting(self):
        def verify(cl, dut):
            cl.enabled.next = True
            cl.s0.next = cl.s1.next = False
            yield cl.clk.negedge
            self.assertEquals(0, cl.out)

            cl.s0.next = True
            yield cl.clk.negedge
            self.assertEquals(1, cl.out)

            cl.s0.next = cl.s1.next = False
            cl.reset.next = True
            yield cl.clk.negedge
            cl.reset.next = False
            yield cl.clk.negedge
            self.assertEquals(0, cl.out)

            cl.s1.next = cl.s0.next = True
            cl.i11.next = 2
            yield cl.clk.negedge
            self.assertEquals(2, cl.out)

            cl.s1.next = True #check if the clk is doing something
            cl.s0.next = False
            pc = 2
            for i in range(64):
                pc += 2
                yield cl.clk.negedge
                self.assertEquals(pc, cl.out)

            cl.enabled.next = False #check if enabled bit is respected
            for i in range(5):
                yield cl.clk.negedge
                self.assertEquals(pc, cl.out)

        genSim(verify).run()

# vim: set ft=python:
