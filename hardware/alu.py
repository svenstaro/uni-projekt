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
            return first * second
        elif opc == 0b0011: #ADN
            return first & ~second
        elif opc == 0b1000: #AND
            return first & second
        elif opc == 0b1001: #ORR
            return first | second
        elif opc == 0b1010: #XOR
            return first ^ second
        elif opc == 0b1011: #NOR
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
        #elif opc == 0b1111: #ROR
        else:
            assert second < bitwidth
            return first << (bitwidth - second) | first >> second

    @always_comb
    def logic():
        Z.next = 0
        N.next = 0
        C.next = 0
        V.next = 0
        Res.next = 0

        if en:
            result = calc(opc, A, B, Cin)
            alu_res = intbv(result)[bitwidth:]

            Z.next = alu_res == 0
            N.next = intbv(alu_res)[bitwidth-1]
            C.next = result & 0x100000000 != 0
            V.next = (A[bitwidth-1] == B[bitwidth-1]) and (A[bitwidth-1] == (not intbv(alu_res)[bitwidth-1]))

            Res.next = alu_res

    return logic
