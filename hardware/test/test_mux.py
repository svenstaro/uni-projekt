from unittest import TestCase
from myhdl import *
from random import randrange
from hardware.mux import *

class DutClass41():
    """Wrapper around DUT"""
    def __init__(self,bitwidth=8):
        self.i00, self.i01, self.i10, self.i11, self.out = [Signal(intbv(0)[bitwidth:]) for _ in range(5)]
        self.s1, self.s0 = [Signal(bool(0)) for _ in range(2)]

    def Gens(self, trace = False):
        self.args = [self.s1,self.s0,self.i00,self.i01,self.i10,self.i11,self.out]

        return traceSignals(mux41, *self.args) if trace else mux41(*self.args)

class DutClass21():
    def __init__(self, bitwidth=8):
        self.i0, self.i1, self.out = [Signal(intbv(0)[bitwidth:]) for _ in range(3)]
        self.s = Signal(bool(0))

    def Gens(self, trace = False):
        self.args = [self.s, self.i0, self.i1, self.out]

        return traceSignals(mux21, *self.args) if trace else mux21(*self.args)

def genSim(verifyMethod, cl=DutClass41, clkfreq=1, trace=False):
    """ Generates a Simulation Object """

    dut_cl = cl()

    @instance
    def stimulus():
        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    dut = dut_cl.Gens(trace=trace)
    return Simulation(dut, stimulus)


class TestMux41(TestCase):
    def testMux(self):
        """Checks if the mux is doing what it is supposed to do"""
        def verify(cl, dut):
            for i in range(128):
                cl.i00.next, cl.i01.next, cl.i10.next, cl.i11.next = [randrange(2**8-1) for _ in range(4)]
                cl.s1.next, cl.s0.next = [randrange(2) for _ in range(2)]
                yield delay(1)

                self.assertEquals({00 : cl.i00, 01 : cl.i01, 10 : cl.i10, 11 : cl.i11}.get(cl.s1 * 10 + cl.s0), cl.out)

        genSim(verify).run()

class TestMux21(TestCase):
    def testMux(self):
        def verify(cl, dut):
            for i in range(128):
                cl.i0.next, cl.i1.next = [randrange(2**8-1) for _ in range(2)]
                cl.s.next = randrange(2)
                yield delay(1)

                self.assertEquals(cl.i1 if cl.s else cl.i0, cl.out)

        genSim(verify, cl=DutClass21).run()

# vim: set ft=python:
