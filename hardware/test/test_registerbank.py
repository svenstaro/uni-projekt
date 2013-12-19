from unittest import TestCase
from myhdl import *
from registerbank import *

class DutClass():
    """Wrapper around DUT"""

    def __init__(self, bitwidth=8, numChannel=5):
        self.clk = Signal(bool(0))
        self.we = Signal(bool(0))
        self.X, self.Y, self.Z = [Signal(intbv(0)[bitwidth:]) for _ in range(3)]
        self.addrX, self.addrY, self.addrZ = [Signal(intbv(0,0,numChannel)) for _ in range(3)]
        self.bitwidth = bitwidth
        self.numChannel = numChannel

    def Gens(self, trace = False):
        args = [self.clk,self.we,self.addrX,self.addrY,self.addrZ,
                self.X,self.Y,self.Z,self.numChannel,self.bitwidth]

        return traceSignals(registerbank, *args) if trace else registerbank(*args)


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


class RegisterbankTest(TestCase):
    def testZeroRegister(self):
        """Check if register 0 is always 0"""

        def verify(cl, dut):
            cl.we.next = True
            cl.addrX.next = 0
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(0, cl.X)

            cl.addrY.next = 0
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(0, cl.Y)

            cl.we.next = False
            cl.addrZ.next = 0
            cl.Z.next = 23
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(0, cl.X)
            self.assertEquals(0, cl.Y)

        genSim(verify).run()

    def testRegisterReadWrite(self):
        """Check if writing and reading register works"""

        def verify(cl, dut):
            cl.addrZ.next = cl.addrX.next = 1
            cl.we.next = True

            cl.Z.next = 34
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(34, cl.X)

            cl.Z.next = 0
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(0, cl.X)

            cl.Z.next = 2**(cl.bitwidth-1)-1
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(2**(cl.bitwidth-1) - 1, cl.X)

            cl.Z.next = 0b11111111
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(0b11111111, cl.X)

            cl.addrX.next = cl.addrZ.next = 2 
            cl.Z.next = 25
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(25, cl.X)

            cl.addrX.next = cl.addrZ.next = 4 
            cl.Z.next = 42
            yield cl.clk.negedge
            yield cl.clk.negedge
            self.assertEquals(42, cl.X)

        genSim(verify).run()

    #def testWriteEnabled(self):
        #"""Test if the write flag is respected"""
        #def verify(cl, dut):
            #cl.we.next = True
            #cl.channel.next = 1

            #cl.Z.next = 20
            #yield cl.clk.negedge
            #yield cl.clk.negedge
            #self.assertEquals(20, cl.out)

            #cl.we.next = False
            #cl.Z.next = 21
            #yield cl.clk.negedge
            #yield cl.clk.negedge
            #self.assertEquals(20, cl.out)

        #genSim(verify).run()

    #def testRegisterAutonomy(self):
        #"""Check if different register give different results"""
        #def verify(cl, dut):
            #cl.we.next = True

            #cl.channel.next = 1
            #cl.Z.next = 1
            #yield cl.clk.negedge
            #yield cl.clk.negedge

            #cl.channel.next = 2
            #cl.Z.next = 2
            #yield cl.clk.negedge
            #yield cl.clk.negedge

            #cl.channel.next = 3
            #cl.Z.next = 3
            #yield cl.clk.negedge
            #yield cl.clk.negedge

            #cl.we.next = False

            #cl.channel.next = 3
            #yield cl.clk.negedge
            #yield cl.clk.negedge
            #self.assertEquals(3, cl.out)

            #cl.channel.next = 2
            #yield cl.clk.negedge
            #yield cl.clk.negedge
            #self.assertEquals(2, cl.out)

            #cl.channel.next = 1
            #yield cl.clk.negedge
            #yield cl.clk.negedge
            #self.assertEquals(1, cl.out)

            #cl.channel.next = 0 #check the 0-register, just to be sure ;)
            #yield cl.clk.negedge
            #yield cl.clk.negedge
            #self.assertEquals(0, cl.out)

        #genSim(verify).run()

    def testReadBeforeWrite(self):
        pass

    def testAddrAutonomy(self):
        pass

# vim: set ft=python:
