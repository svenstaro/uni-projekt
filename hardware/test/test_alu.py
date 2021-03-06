# -*- coding: utf-8 -*-

from unittest import TestCase
from myhdl import *
from hardware.alu import *

class DutClass():
    """Wrapper around DUT"""
    def __init__(self):
        self.en, self.z, self.n, self.cin, self.v = [Signal(bool(0)) for _ in range(5)]
        self.cout = Signal(bool(0))

        self.opc = Signal(intbv(0)[4:])
        self.A, self.B= [Signal(intbv(0)[32:]) for _ in range(2)]
        self.R = Signal(modbv(0, 0, 2**32))

    def Gens(self, trace = False):
        self.args = [self.opc,self.en,self.A,self.B,self.cout,self.R,
                self.z,self.n,self.cin,self.v]

        return traceSignals(alu, *self.args) if trace else alu(*self.args)

def genSim(verifyMethod, cl=DutClass, clkfreq=1, trace=False):
    """ Generates a Simulation Object """

    dut_cl = cl()

    @instance
    def stimulus():
        dut_cl.en.next = True
        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    dut = dut_cl.Gens(trace=trace)
    return Simulation(dut, stimulus)

class TestAluArithmetic(TestCase):
    def testArithmetic(self):
        """Test if the arithmetic works"""
        def verify(cl, dut):
            #first opcode, then a tuple of A, B, C, Res
            tests = {
                0b0000: [(10,23,0,33), #ADD
                         (0,0,0,0),
                         (-3,-10,0,-13),
                         (-5,3,0,-2),
                         (3,-40,0,-37),
                         (23,8,1,31)], #check if carry is wayne
                0b0001: [(10,11,1,22), #ADC
                         (0,0,1,1),
                         (-10,9,1,0),
                         (10,3,0,13)],
                0b0100: [(10,3,0,7), #SUB
                         (-7,-3,0,-4),
                         (0,-10,0,10),
                         (-5,3,1,-8)],
                0b0101: [(-10,-3,1,-8), #SBC
                         (5,3,1,1)],
                0b0110: [(6,3,0,-3), #RSB
                         (5,10,0,5),
                         (13,-13,1,-26)],
                0b0111: [(4,5,1,2), #RSC
                         (23,20,1,-2),
                         (-5,-7,1,-1)],
                0b0010: [(4,5,0,20), #MUL
                         (-3,4,0,-12),
                         (6,-3,0,-18),
                         (-3,-3,0,9)],
                }

            for opc, val in tests.iteritems():
                for tup in val:
                    cl.opc.next = opc
                    cl.A.next = intbv(tup[0])[32:]
                    cl.B.next = intbv(tup[1])[32:]
                    cl.cout.next = tup[2]
                    yield delay(1)
                    #self.assertEquals(tup[3], cl.R, msg = "%s != %s (%s⊕%s⊕%s opc:%s) " % (tup[3],cl.R,cl.A,cl.B,cl.cout,bin(opc,4)))
                    self.assertEquals(tup[3], cl.R.signed())

        genSim(verify).run()

    def testLogic(self):
        """Check the logic components of the alu"""
        def verify(cl, dut):
            #opcode, A, B, result
            tests = {
                0b0011: [(0b0101, 0b1000, 0b0101), #ADN
                         (0b0000, 0b0000, 0b0000),
                         (0b1001, 0b0000, 0b1001)],
                0b1000: [(0b0010, 0b1111, 0b0010), #AND
                         (0b1100, 0b0101, 0b0100),
                         (0b1110, 0b0001, 0b0000)],
                0b1001: [(0b0001, 0b0010, 0b0011), #ORR
                         (0b0000, 0b0101, 0b0101)],
                0b1010: [(0b0000, 0b1010, 0b1010), #XOR
                         (0b1111, 0b0110, 0b1001)],
                0b1011: [(0b0000, 0b0000, intbv(-1))] #ORN
                }

            for opc, val in tests.iteritems():
                for tup in val:
                    cl.opc.next = opc
                    cl.A.next = tup[0]
                    cl.B.next = tup[1]
                    yield delay(1)
                    #self.assertEquals(tup[2], cl.R, msg = "%s != %s (%s⊕%s opc:%s) " % (tup[2],cl.R,cl.A,cl.B,bin(opc,4)))
                    self.assertEquals(tup[2], cl.R.signed())

        genSim(verify).run()

    def testShiftRotate(self):
        """Check if the shift/rotation works correctly"""
        def verify(cl, dut):
            #opcode, A, B, result
            tests = {
                0b1100: [(1,3, 0b1000), #LSL
                         (5,4, 0b1010000),
                         (13,0,13),
                         (0,5,0),
                         (16,30,0),
                         (1,31,-2**31)],
                0b1101: [(1,0, 1), #ASR
                         (3,10,0),
                         (10,1,0b101),
                         (~1,2,-1),
                         (~1,0,~1),
                         (-1,31,-1)],
                0b1110: [(-1,31,1), #LSR
                         (3,10,0),
                         (6,0,6),
                         (-1,0,-1),
                         (5,1,2)],
                0b1111: [(4,29,32),
                         (6,1,3)]  #ROR
                }

            for opc, val in tests.iteritems():
                for tup in val:
                    cl.opc.next = opc
                    cl.A.next = intbv(tup[0])[32:]
                    cl.B.next = intbv(tup[1])[32:]
                    yield delay(1)
                    #self.assertEquals(tup[2], cl.R.signed(), msg = "%s != %s (%s⊕%s opc:%s) " % (tup[2],cl.R,cl.A,cl.B,bin(opc,4)))
                    self.assertEquals(tup[2], cl.R.signed())

        genSim(verify).run()

    def testStatusFlags(self):
        """Check if the status flags are set properly"""
        def verify(cl, dut):
            """@type cl: DutClass"""

            n = None
            t = True
            f = False

            # opcode:    (A, B, Cin, R, Z, N, C, V)
            cases = {
                0b0000: [(0, 0, f, 0, t, f, f, f)], #add
                0b0100: [(0, 1, f, n, f, t, f, t)], #sub
                0b1111: [(1, 1, f, n, n, t, f, t)]  #ror
            }

            cl.en.next = True
            for opc,tests in cases.iteritems():
                cl.opc.next = opc
                for e in tests:
                    assert 8 == len(e)  # do we have all in-/outputs?

                    cl.A.next = e[0]
                    cl.B.next = e[1]
                    cl.cin.next = e[2]

                    yield delay(1)

                    if e[3] is not None:
                        self.assertEquals(e[3], cl.R)
                    if e[4] is not None:
                        self.assertEquals(e[4], cl.z)
                    if e[5] is not None:
                        self.assertEquals(e[5], cl.n)
                    if e[6] is not None:
                        self.assertEquals(e[6], cl.cout)
                    if e[7] is not None:
                        self.assertEquals(e[7], cl.v)


        genSim(verify).run()
