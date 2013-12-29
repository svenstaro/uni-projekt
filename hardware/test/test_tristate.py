from unittest import TestCase
from myhdl import *
from tristate import *

class DutClass():
    """Wrapper around DUT"""
    def __init__(self):
        self.input, self.input2 = [Signal(intbv(0)[32:]) for _ in range(2)]
        self.en, self.en2 = [Signal(bool(0)) for _ in range(2)]
        self.output = TristateSignal(intbv(0)[32:])

    def Gens(self, trace = False):
        self.args  = [self.input,self.en,self.output.driver()]
        args2 = [self.input2,self.en2,self.output.driver()]

        return traceSignals(tristate, *self.args) if trace else tristate(*self.args), traceSignals(tristate, *args2) if trace else tristate(*args2)

def genSim(verifyMethod, cl=DutClass, clkfreq=1, trace=False):
    """ Generates a Simulation Object """

    dut_cl = cl()

    @instance
    def stimulus():
        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    dut = dut_cl.Gens(trace=trace)
    return Simulation(dut, stimulus)


class TristateTest(TestCase):
    def testTristate(self):
        """Tests if the tristate works correctly"""
        def verify(cl, dut):
            cl.en.next = False
            cl.input.next = 0b1110001
            yield delay(1)
            self.assertEquals(None, cl.output)

            cl.en.next = True
            yield delay(1)
            self.assertEquals(0b1110001, cl.output)

            cl.en.next = False
            cl.en2.next = True
            cl.input2.next = 0b1100
            yield delay(1)
            self.assertEqual(0b1100, cl.output)

            cl.en2.next = False
            yield delay(1)
            self.assertEquals(None, cl.output)

        genSim(verify).run()
