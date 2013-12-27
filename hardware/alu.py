from myhdl import *

def alu(opc, A, B, Cin, Res, Z, N, C, V, bitwidth=32):
    """This represents the ALU of the microcontroller.

    All Parameters are Signals as usual.

    opc (I4)    -- The opcode (must be a valid alu opcode)
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
        result = 0
        a = A.signed()
        b = B.signed()

        if   opc == 0b0000: #ADD
            result = a + b
        elif opc == 0b0001: #ADC
            result = a + b + Cin
        elif opc == 0b0100: #SUB
            result = a - b
        elif opc == 0b0101: #SBC
            result = a - b - Cin
        elif opc == 0b0110: #RSB
            result = b - a
        elif opc == 0b0111: #RSC
            result = b + Cin - a
        elif opc == 0b0010: #MUL
            result = a * b  #TODO hardware nutzen
        elif opc == 0b0011: #ADN
            result = a & ~b
        elif opc == 0b1000: #AND
            result = a & b
        elif opc == 0b1001: #ORR
            result = a | b
        elif opc == 0b1010: #XOR
            result = a ^ b
        elif opc == 0b1011: #NOT
            result = a | ~b
        elif opc == 0b1100: #LSL
            result = a << b
        elif opc == 0b1101: #ASR
            result = a >> b
        elif opc == 0b1110: #LSR
            result = ((intbv(a)[bitwidth+1:] & (2**bitwidth-1)) >> b)[bitwidth:] #TODO unhuebsch
        elif opc == 0b1111: #ROR
            result = a << (bitwidth + ~b + 1)
        else:
            assert False

        amsb = A[bitwidth-1]
        bmsb = B[bitwidth-1]
        rmsb = intbv(result)[bitwidth-1]

        Z.next = result == 0
        N.next = result < 0
        C.next = intbv(result)[bitwidth]
        V.next = (amsb == bmsb) and (amsb == (not rmsb))

        Res.next = intbv(result)[bitwidth:]

    return logic
