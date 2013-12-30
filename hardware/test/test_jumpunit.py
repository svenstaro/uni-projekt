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
    def testJumpUnit(self):
        def verify(cl, dut):
            assert isinstance(cl, DutClass)

            tests = [(0b00000, 0,0,0,0, 0),
                     (0b00001, 0,0,0,0, 1),
                     (0b00010, 0,0,0,0, 0),
                     (0b00010, 0,0,0,1, 1),
                     (0b00011, 0,0,0,0, 1),
                     (0b00011, 0,0,0,1, 0),
                    ]

            for t in tests:
                cl.code.next = t[0]
                cl.Z.next = t[1]
                cl.N.next = t[2]
                cl.C.next = t[3]
                cl.V.next = t[4]
                yield delay(1)
                self.assertEquals(t[5], cl.out, msg="%s != %s %s %s %s %s %s" % (cl.out, bin(t[0],width=5),t[1],t[2],t[3],t[4],t[5]))


        genSim(verify).run()

# vim: set ft=python:
