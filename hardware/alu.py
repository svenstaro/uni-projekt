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

    def calc(opc, first, second, c):
        if   opc == 0b0000: #ADD
            return first + second
        elif opc == 0b0001: #ADC
            return first + second + c
        elif opc == 0b0100: #SUB
            return first - second
        elif opc == 0b0101: #SBC
            return first - second - c
        elif opc == 0b0110: #RSB
            return second - first
        elif opc == 0b0111: #RSC
            return second + c - first
        elif opc == 0b0010: #MUL
            return first.signed() * second.signed()
        elif opc == 0b0011: #ADN
            return first & ~second
        elif opc == 0b1000: #AND
            return first & second
        elif opc == 0b1001: #ORR
            return first | second
        elif opc == 0b1010: #XOR
            return first ^ second
        elif opc == 0b1011: #NOT
            return first | ~second
        elif opc == 0b1100: #LSL
            assert second < bitwidth
            return first << second
        elif opc == 0b1101: #ASR
            assert second < bitwidth
            return first.signed() >> second
        elif opc == 0b1110: #LSR
            assert second < bitwidth
            return first >> second
        elif opc == 0b1111: #ROR
            assert second < bitwidth
            return first << (bitwidth - second) | first >> second

    @always_comb
    def logic():
        if en:
            alu_res = calc(opc, A, B, Cin)

            Z.next = alu_res == 0
            N.next = intbv(alu_res)[bitwidth-1]
            C.next = intbv(alu_res)[bitwidth]
            V.next = (A[bitwidth-1] == B[bitwidth-1]) and (A[bitwidth-1] == (not intbv(alu_res)[bitwidth-1]))

            Res.next = alu_res

    return logic
