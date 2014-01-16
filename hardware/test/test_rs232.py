from unittest import TestCase
from myhdl import *
from hardware.rs232tx import *
from hardware.rs232rx import *

class DutClass():
    """Wrapper around DUT"""
    def __init__(self):
        self.clk = Signal(bool(0))
        self.reset = ResetSignal(0, 1, True)
        self.write, self.available, self.ready = [Signal(bool(0)) for _ in range(3)]
        self.dataIn, self.dataOut = [Signal(intbv(0)[32:]) for _ in range(2)]
        self.wire = Signal(bool(1))

    def Gens(self, trace = False):
        argst = [self.clk,self.reset,self.ready,self.write,self.dataIn,self.wire, 50, 10]
        argsr = [self.clk,self.reset,self.wire,self.dataOut,self.available, 50, 10]

        result = rs232tx(*argst), rs232rx(*argsr)
        return result

def genSim(verifyMethod, cl=DutClass, clkfreq=1, trace=False):
    """ Generates a Simulation Object """

    dut_cl = cl()

    @always(delay(clkfreq))
    def clkGen():
        dut_cl.clk.next = not dut_cl.clk

    @instance
    def stimulus():
        dut_cl.reset.next = True
        yield delay(5*clkfreq)
        dut_cl.reset.next = False

        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    dut = traceSignals(dut_cl.Gens) if trace else dut_cl.Gens()
    return Simulation(dut, clkGen, stimulus)


class Rs232Test(TestCase):
    def testIt(self):
        def verify(cl, dut):
            assert isinstance(cl, DutClass)

            tests = [170, 85, 219, 60, 255, 0, 255]

            for t in tests:
                cl.write.next = True
                cl.dataIn.next = t
                yield delay(2)
                cl.write.next = False
                yield cl.available.posedge
                self.assertEquals(t, cl.dataOut)
                yield delay(int(1.5*50/10))

        genSim(verify, trace=True).run()
