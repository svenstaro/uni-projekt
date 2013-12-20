from math import log
from myhdl import *

def alu(opc, ups, A, B, Cin, Res, Z, N, C, V, bitwidth=32):
    """This represents the ALU of the microcontroller.

    All Parameters are Signals as usual.

    opc (I4)    -- The opcode (must be a valid alu opcode)
    ups (Ibool) -- Signal which says if to update the status flags
    A   (Obw)   -- First input - must be modbv
    B   (Obw)   -- Second input - must be modbv
    Cin (Ibool) -- Carry input
    Res (Obw)   -- The Result
    Z   (Obool) -- Zero flag
    N   (Obool) -- Negative flag
    C   (Obool) -- Carry flag
    V   (Obool) -- Overflow flag
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
        return B + Cin - A

    def MUL(A, B, Cin):
        return A * B #TODO hardware nutzen
    def DIV(A, B, Cin):
        return A // B #TODO rauswerfen

    def AND(A, B, Cin):
        return A & B
    def ORR(A, B, Cin):
        return A | B
    def XOR(A, B, Cin):
        return A ^ B
    def NOT(A, B, Cin):
        return ~B

    def LSL(A, B, Cin):
        return (A << B)[bitwidth:].signed()
    def ASR(A, B, Cin):
        return A >> B
    def LSR(A, B, Cin):
        return ((A[bitwidth+1:] & (2**bitwidth-1)) >> B)[bitwidth:].signed() #TODO unhuebsch
    def ROR(A, B, Cin):
        return A << (bitwidth - B)


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
            amsb = A[bitwidth-1]
            bmsb = B[bitwidth-1]
            rmsb = intbv(result)[bitwidth-1]

            Z.next = result == 0
            N.next = result < 0
            C.next = intbv(result)[bitwidth]
            V.next = (amsb == bmsb) and (amsb == (not rmsb))

        Res.next = result

    return logic
