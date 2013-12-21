from myhdl import *

def alu(opc, ups, A, B, Cin, Res, Z, N, C, V, bitwidth=32):
    """This represents the ALU of the microcontroller.

    All Parameters are Signals as usual.

    opc (I4)    -- The opcode (must be a valid alu opcode)
    ups (Ibool) -- Signal which says if to update the status flags
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

        if   opc == 0b000:
            result =  A + B
        elif opc == 0b001:
            result = A + B + Cin
        elif opc == 0b0100:
            result = A - B
        elif opc == 0b0101:
            result = A - B - Cin
        elif opc == 0b0110:
            result = B - A
        elif opc == 0b0111:
            result = B + Cin - A
        elif opc == 0b0010:
            result = A * B  #TODO hardware nutzen
        elif opc == 0b0011:
            result = A // B #TODO rauswerfen
        elif opc == 0b1000:
            result = A & B
        elif opc == 0b1001:
            result = A | B
        elif opc == 0b1010:
            result = A ^ B
        elif opc == 0b1011:
            result = ~B
        elif opc == 0b1100:
            result = (A << B)[bitwidth:].signed()
        elif opc == 0b1101:
            result = A >> B
        elif opc == 0b1110:
            result = ((A[bitwidth+1:] & (2**bitwidth-1)) >> B)[bitwidth:].signed() #TODO unhuebsch
        elif opc == 0b1111:
            result = A << (bitwidth - B)

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
