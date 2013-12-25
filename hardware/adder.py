from myhdl import *

def adder(A, B, S):
    """Simple adder without carry or antyhing

    All parameters are Signals as usual

    A (I)   -- First input
    B (I)   -- Second input
    S (O)   -- Result A+B

    """

    @always_comb
    def logic():
        S.next = A + B

    return logic

def adderC(A, B, cin, S, cout, bitwidth=32):
    """Simple fulladder with carryin and carryout

    All parameters are Signals as usual

    A (I)   -- First input
    B (I)   -- Second input
    cin     -- Carry in
    S (O)   -- Result A+B
    cout    -- Carry out
    """

    @always_comb
    def logic():
        S.next = A + B
        cout.next = intbv(A + B)[bitwidth]

    return logic
