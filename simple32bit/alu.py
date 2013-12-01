from math import log
from myhdl import *

def alu(clk, opc, upS, A, B, Cin, Res, Z, N, C, V):
    """This represents the ALU of the microcontroller.

    All Parameters are Signals as usual.

    clk -- The clock
    opc -- The opcode (must be a valid alu opcode)
    upS -- Signal which says if to update the status flags
    A   -- First input
    B   -- Second input
    Cin -- Carry input
    Res -- The Result
    Z   -- Zero flag
    N   -- Negative flag
    C   -- Carry flag
    V   -- Overflow flag
    """
    def ADD(A, B, Cin):
        return A + B
    def ADDC(A, B, Cin):
        return A + B + Cin
    def SUB(A, B, Cin):
        return A - B
    def SBC(A, B, Cin):
        return A - B - C

    def MUL(A, B, Cin):
        return A * B #TODO
    def MLL(A, B, Cin):
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
        return ~B #TODO

    def LSL(A, B, Cin):
        return A << B
    def ASR(A, B, Cin):
        return A >> B
    def LSR(A, B, Cin):
        return 0 #TODO
    def ROR(A, B, Cin):
        return 0 #TODO


    opcodes = { 
                #arithmetic
                0b00000 : ADD,
                0b00001 : ADC,
                0b00100 : SUB,
                0b00101 : SBC,
                0b00110 : RSB,
                0b00111 : RSC,
                #arithm special
#                0b10000 : MUL,
#                0b10001 : MLL,
#                0b10010 : DIV,
                #logic
                0b01000 : AND,
                0b01001 : ORR,
                0b01010 : XOR,
                0b01011 : NOT,
                #shift/rotate
                0b01100 : LSL,
                0b01101 : ASR,
                0b01110 : LSR,
                0b01111 : ROR
              }

    @always_seq(clk.posedge)
    def logic():
        assert opc+0 in opcodes #dirty hack

        Res.next = opcodes[opc](A, B, Cin)
        
        if upS: #update status flags
            Z.next = Res.next == 0
            N.next = Res.next[math.log(Res.next.max, 2) - 1]
            C.next = 0 #TODO
            V.next = 0 #TODO 

    return logic

