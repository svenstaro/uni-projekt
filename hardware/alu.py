from math import log
from myhdl import *

def alu(opc, ups, A, B, Cin, Res, Z, N, C, V):
    """This represents the ALU of the microcontroller.

    All Parameters are Signals as usual.

    opc -- The opcode (must be a valid alu opcode)
    ups -- Signal which says if to update the status flags
    A   -- First input - must be modbv
    B   -- Second input - must be modbv
    Cin -- Carry input
    Res -- The Result
    Z   -- Zero flag
    N   -- Negative flag
    C   -- Carry flag
    V   -- Overflow flag
    """

    def ADD(A, B, Cin):
        return A + B
    def ADC(A, B, Cin):
        return A + B + Cin
    def SUB(A, B, Cin):
        return A - B
    def SBC(A, B, Cin):
        return A - B - Cin
    def RSB(A, B, Cin):
        return B - A
    def RSC(A, B, Cin):
        return B - A - Cin

    def MUL(A, B, Cin):
        return A * B #TODO
    def DIV(A, B, Cin):
        return A // B #TODO

    def AND(A, B, Cin):
        return A & B
    def ORR(A, B, Cin):
        return A | B
    def XOR(A, B, Cin):
        return A ^ B
    def NOT(A, B, Cin):
        return ~B

    def LSL(A, B, Cin):
        return A << B
    def ASR(A, B, Cin):
        return A >> B
    def LSR(A, B, Cin):
        return 0 #TODO
    def ROR(A, B, Cin):
        return A << (32 - B)


    opcodes = {
                #arithmetic
                0b0000 : ADD,
                0b0001 : ADC,
                0b0100 : SUB,
                0b0101 : SBC,
                0b0110 : RSB,
                0b0111 : RSC,
                #arithm special
                0b0010 : MUL,
                0b0011 : DIV,
                #logic
                0b1000 : AND,
                0b1001 : ORR,
                0b1010 : XOR,
                0b1011 : NOT,
                #shift/rotate
                0b1100 : LSL,
                0b1101 : ASR,
                0b1110 : LSR,
                0b1111 : ROR
              }

    @always_comb
    def logic():
        assert int(opc) in opcodes

        result = opcodes[int(opc)](A, B, Cin)

        if ups: #update status flags
            Z.next = result == 0
            N.next = result < 0
            C.next = A[len(A)] ^ B[len(B)]
            V.next = False #TODO

        Res.next = result

    return logic

