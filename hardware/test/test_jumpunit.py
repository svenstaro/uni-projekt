from unittest import TestCase
from myhdl import *
from jumpunit import *

class DutClass():
    """Wrapper around DUT"""
    def __init__(self):
        self.code = Signal(intbv(0)[5:])
        self.Z, self.N, self.C, self.V, self.out = [Signal(bool(0)) for _ in range(5)]

    def Gens(self, trace = False):
        self.args = [self.code, self.Z, self.N, self.C, self.V, self.out]
        
        return traceSignals(jumpunit, *self.args) if trace else jumpunit(*self.args)

def genSim(verifyMethod, cl=DutClass, clkfreq=1, trace=False):
    """ Generates a Simulation Object """

    dut_cl = cl()

    @instance
    def stimulus():
        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    dut = dut_cl.Gens(trace=trace)
    return Simulation(dut, stimulus)


class JumpUnitTest(TestCase):
    def testSomething(self):
        def verify(cl, dut):
            for _ in range(200):
                cl.C.next = not cl.C
                yield delay(1)

        genSim(verify).run()

# vim: set ft=python:
