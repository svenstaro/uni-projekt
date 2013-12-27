from unittest import TestCase
from myhdl import *
from pc import *
from adder import *
from pc import programcounter


class DutClass():
    """Wrapper around DUT"""
    def __init__(self):
        self.clk = Signal(bool(0))
        self.reset = ResetSignal(0, 1, True)

        self.enabled, self.cpucall, self.jumpunit, self.cpujump, self.op1 = [Signal(bool(0)) for _ in range(5)]
        self.imm24 = Signal(intbv(0)[24:])
        self.reg   = Signal(intbv(0)[32:])
        self.out   = Signal(intbv(0)[32:])
        self.args = [self.clk, self.reset, self.enabled, self.imm24, self.reg, self.cpucall, self.jumpunit,
                self.cpujump, self.op1, self.out]

    def Gens(self, trace = False):
        return traceSignals(programcounter, *self.args) if trace else programcounter(*self.args)

def genSim(verifyMethod, cl=DutClass, clkfreq=1, trace=False):
    """ Generates a Simulation Object """

    dut_cl = cl()

    @always(delay(clkfreq))
    def clkGen():
        dut_cl.clk.next = not dut_cl.clk

    @instance
    def stimulus():
        #dut_cl.reset.next = True
        #yield delay(3*clkfreq)
        #dut_cl.reset.next = False

        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    dut = dut_cl.Gens(trace=trace)
    return Simulation(dut, clkGen, stimulus)


class TestPc(TestCase):
    def testCounting(self):
        def verify(cl, dut):
            assert isinstance(cl, DutClass)
            cl.enabled.next = True

            pc = 0
            cl.cpujump.next = False #check if the clk is doing something
            for i in range(64):
                if i % 2 == 0:
                    cl.jumpunit.next = True
                else:
                    cl.jumpunit.next = False #check if jumpunit is making any difference (it should not!)
                pc += 4
                yield cl.clk.negedge
                self.assertEquals(pc, cl.out)

            cl.enabled.next = False #check if enabled bit is respected
            for i in range(5):
                yield cl.clk.negedge
                self.assertEquals(pc, cl.out)

            cl.enabled.next = True
            cl.cpujump.next = True
            cl.jumpunit.next = True
            cl.op1.next = False
            cl.reg.next = 178
            yield cl.clk.negedge
            self.assertEquals(178, cl.out)

            cl.op1.next = True
            cl.imm24.next = 22
            yield  cl.clk.negedge
            self.assertEquals(200, cl.out)

        genSim(verify).run()

# vim: set ft=python:
