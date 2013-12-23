from myhdl import *

def jumpunit(code, Z, N, C, V, out):
    """This jumpunit determines if the condition for jumping is met

    code (I5) -- The inputcode
    Z    (I1) -- Zero flag
    N    (I1) -- Negative flag
    C    (I1) -- Carry flag
    V    (I1) -- Overflow flag
    out  (O1) -- The result
    """

    @always_comb
    def logic():
        result = False
        if code[4]:
            result |= Z
        if code[3]:
            result |= N
        if code[2]:
            result |= C
        if code[1]:
            result |= V
        if code[0]:
            result = not result

        out.next = result

    return logic
