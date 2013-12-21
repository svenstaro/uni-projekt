from unittest import TestCase
from myhdl import *
from irdecoder import *

class DutClass():
    """Wrapper around DUT"""
    def __init__(self):
        self.ir = Signal(intbv(0)[32:])
        self.aluop, self.dest, self.source, self.source2 = [Signal(intbv(0)[4:]) for _ in range(4)]
        self.op1, self.op2, self.statusUp = [Signal(intbv(0)[1:]) for _ in range(3)]
        self.imm24 = Signal(intbv(0)[24:])
        self.imm16 = Signal(intbv(0)[16:])

    def Gens(self, trace = False):
        args = [self.ir,self.aluop,self.dest,self.source,self.op1,
                self.op2,self.source2,self.imm24,self.imm16,self.statusUp]
        return traceSignals(irdecoder, *args) if trace else irdecoder(*args)

def genSim(verifyMethod, cl=DutClass, clkfreq=1, trace=False):
    """ Generates a Simulation Object """

    dut_cl = cl()

    @instance
    def stimulus():
        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    dut = dut_cl.Gens(trace=trace)
    return Simulation(dut, stimulus)


class TestIrDecoder(TestCase):
    def testDecoding(self):
        """Check if the irdecoder gives the correct aluop, op2, etc"""
        def verify(cl, dut):
            order = [
                   #(0, cl.ir),
                    (1, cl.aluop),
                    (2, cl.dest),
                    (3, cl.source),
                    (4, cl.op1),
                    (5, cl.op2),
                    (6, cl.source2),
                    (7, cl.imm24),
                    (8, cl.imm16),
                    (9, cl.statusUp)
                ]

            tests = [
                #for order see 'order'
                #'x' means "don't care"

                ('00 0000 1 0001 0010 0 0000 0000 0000 0100', 
                    0b0000, 0b0001, 0b0010, 'x', 0, 0b0100, 'x', 'x', 1),
                ('00 0100 0 1111 0000 1 1000 0000 0010 1111',
                    0b0100, 0b1111, 0b0000, 'x', 1, 'x', 'x', 0b1000000000101111, 0),
                ('00 0111 1 0000 1111 1 1111 1111 0000 1111',
                    0b0111, 0b000, 0b1111, 'x', 1, 'x', 'x', 0b1111111100001111, 1),
                ('00 1010 0 1100 0011 0 0000 0000 0000 1111',
                    0b1010, 0b1100, 0b0011, 'x', 0, 0b1111, 'x', 'x', 0),
                ('11 00100 0 0000 0000 0000 0000 0000 1111',
                    'x', 'x', 'x', 0, 'x', 0b1111, 'x', 'x', 'x'),
                ('11 00101 1 1100 0011 1010 0101 1111 0000',
                    'x', 'x', 'x', 1, 'x', 'x', 0b110000111010010111110000, 'x', 'x')
                ]

            for t in tests:
                assert len(t) == 10 #check that we have preset all ports

                cl.ir.next = int(t[0].replace(' ', ''),2) if type(t[0]) == str else t[0]
                yield delay(1)

                for ind,port in order:
                    if type(t[ind]) is str: #convert strings to int
                        if t[ind] == 'x': 
                            continue
                        else:
                            bs = t[ind].replace(' ', '')
                            assert len(bs) == 32
                            num = int(bs, 2)
                    else:
                        num = t[ind]

                    self.assertEquals(num, port)

        genSim(verify).run()

# vim: set ft=python: