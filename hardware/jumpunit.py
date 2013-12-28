from myhdl import *

def jumpunit(code, Z, N, C, V, R):
    """This jumpunit determines if the condition for jumping is met

    code (I5) -- The inputcode
    Z    (I1) -- Zero flag
    N    (I1) -- Negative flag
    C    (I1) -- Carry flag
    V    (I1) -- Overflow flag
    R    (O1) -- The result
    """

    @always_comb
    def logic():
        result = False
        if code[4]:
            result = result or bool(Z)
        if code[3]:
            result = result or bool(N)
        if code[2]:
            result = result or bool(C)
        if code[1]:
            result = result or bool(V)
        if code[0]:
            result = not result

        R.next = result

    return logic
