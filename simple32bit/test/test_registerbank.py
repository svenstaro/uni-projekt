from unittest import TestCase
from myhdl import *
from registerbank import *

class DutClass():
    """Wrapper around DUT"""

    def __init__(self, bitwidth=8, numChannel=5):
        self.clk = Signal(bool(0))
        self.reset = ResetSignal(0,1,True)
        self.we = Signal(bool(0))
        self.inn = Signal(intbv(0)[bitwidth:])
        self.out = Signal(intbv(0)[bitwidth:])
        self.channel = Signal(intbv(0,0,numChannel))
        self.bitwidth = bitwidth
        self.numChannel = numChannel

    def Gens(self, trace = False):
        args = [self.clk, self.reset,self.we,self.channel,
                self.inn,self.out,self.numChannel,self.bitwidth]

        return traceSignals(registerbank, *args) if trace else registerbank(*args)


def genSim(verifyMethod, cl=DutClass, clkfreq=1, trace=False):
    """ Generates a Simulation Object """

    dut_cl = cl()

    @always(delay(clkfreq))
    def clkGen():
        dut_cl.clk.next = not dut_cl.clk

    @instance
    def stimulus():
        dut_cl.reset.next = True
        yield delay(3)
        dut_cl.reset.next = False

        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    dut = dut_cl.Gens(trace=trace)
    return Simulation(dut, clkGen, stimulus)


class RegisterbankTest(TestCase):
    def testZeroRegister(self):
        """Check if register 0 is always 0"""

        def verify(cl, dut):
            cl.we.next = True
            cl.inn.next = intbv(1)
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(0, cl.out)

            cl.inn.next = intbv(30)
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(0, cl.out)

            cl.we.next = False
            cl.inn.next = intbv(22)
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(0, cl.out)

        genSim(verify).run()

    def testRegisterReadWrite(self):
        """Check if writing and reading register works"""

        def verify(cl, dut):
            cl.channel.next = 1
            cl.we.next = True

            cl.inn.next = intbv(23)
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(23, cl.out)

            cl.inn.next = intbv(0)
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(0, cl.out)

            cl.inn.next = intbv(2**cl.bitwidth - 1)
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(2**cl.bitwidth - 1, cl.out)

            cl.channel.next = 2 
            cl.inn.next = intbv(25)
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(25, cl.out)

            cl.channel.next = 4 
            cl.inn.next = intbv(42)
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(42, cl.out)

        genSim(verify).run()

    def testWriteEnabled(self):
        """Test if the write flag is respected"""
        def verify(cl, dut):
            cl.we.next = True
            cl.channel.next = 1

            cl.inn.next = intbv(20)
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(20, cl.out)

            cl.we.next = False
            cl.inn.next = intbv(21)
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(20, cl.out)

        genSim(verify).run()

    def testRegisterAutonomy(self):
        """Check if different register give different results"""
        def verify(cl, dut):
            cl.we.next = True

            cl.channel.next = 1
            cl.inn.next = intbv(1)
            yield cl.clk.negedge
            yield cl.clk.negedge

            cl.channel.next = 2
            cl.inn.next = intbv(2)
            yield cl.clk.negedge
            yield cl.clk.negedge

            cl.channel.next = 3
            cl.inn.next = intbv(3)
            yield cl.clk.negedge
            yield cl.clk.negedge

            cl.we.next = False

            cl.channel.next = 3
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(3, cl.out)

            cl.channel.next = 2
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(2, cl.out)

            cl.channel.next = 1
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(1, cl.out)

            cl.channel.next = 0 #check the 0-register, just to be sure ;)
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(0, cl.out)

        genSim(verify).run()


# vim: set ft=python:
