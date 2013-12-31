from myhdl import *

def alu(opc, en, A, B, Cin, Res, Z, N, C, V, bitwidth=32):
    """This represents the ALU of the microcontroller.

    All Parameters are Signals as usual.

    opc (I4)    -- The opcode (must be A valid alu opcode)
    A   (Obw)   -- First input
    B   (Obw)   -- Second input
    Cin (Ibool) -- Carry input
    Res (Obw)   -- The Result
    Z   (Obool) -- Zero flag
    N   (Obool) -- Negative flag
    C   (Obool) -- Carry flag
    V   (Obool) -- Overflow flag
    """

    @always_comb
    def logic():
        if en:
            result = 0

            if   opc == 0b0000: #ADD
                result = A + B
            elif opc == 0b0001: #ADC
                result = A + B + Cin
            elif opc == 0b0100: #SUB
                result = A - B
            elif opc == 0b0101: #SBC
                result = A - B - Cin
            elif opc == 0b0110: #RSB
                result = B - A
            elif opc == 0b0111: #RSC
                result = B + Cin - A
            elif opc == 0b0010: #MUL
                result = A * B  #TODO hardware nutzen
            elif opc == 0b0011: #ADN
                result = A & ~B
            elif opc == 0b1000: #AND
                result = A & B
            elif opc == 0b1001: #ORR
                result = A | B
            elif opc == 0b1010: #XOR
                result = A ^ B
            elif opc == 0b1011: #NOT
                result = A | ~B
            elif opc == 0b1100: #LSL
                assert B < 32
                result = A << B
            elif opc == 0b1101: #ASR
                assert B < 32
                result = A.signed() >> B
            elif opc == 0b1110: #LSR
                assert B < 32
                result = A >> B
            elif opc == 0b1111: #ROR
                assert bitwidth >= B
                result = A << (bitwidth - B) | A >> B
            else:
                assert False

            Z.next = result == 0
            N.next = result < 0
            #C.next = intbv(result)[bitwidth]
            #V.next = (A[bitwidth-1] == B[bitwidth-1]) and (A[bitwidth-1] == (not intbv(result)[bitwidth-1]))

            Res.next = result

    return logic
