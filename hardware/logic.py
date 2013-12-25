from myhdl import *

def contradiction(A, B, R):

    @always_comb
    def logic():
        R.next = 0

    return logic

def nor(A, B, R):

    @always_comb
    def logic():
        R.next = ~(A | B)

    return logic

def xB(A, B, R):

    @always_comb
    def logic():
        R.next = ~(~A | B)

    return logic

def nA(A, B, R):

    @always_comb
    def logic():
        R.next = ~A

    return logic

def xA(A, B, R):

    @always_comb
    def logic():
        R.next = A & ~B

    return logic

def nB(A, B, R):

    @always_comb
    def logic():
        R.next = ~B

    return logic

def xor(A, B, R):

    @always_comb
    def logic():
        R.next = A ^ B

    return logic

def nand(A, B, R):

    @always_comb
    def logic():
        R.next = ~(A & B)

    return logic

def andd(A, B, R):

    @always_comb
    def logic():
        R.next = A & B

    return logic

def xnor(A, B, R):

    @always_comb
    def logic():
        R.next = ~(A ^ B)

    return logic

def A(A, B, R):

    @always_comb
    def logic():
        R.next = A

    return logic

def impl(A, B, R):

    @always_comb
    def logic():
        R.next = ~A | B

    return logic

def B(A, B, R):

    @always_comb
    def logic():
        R.next = B

    return logic

def xnB(A, B, R):

    @always_comb
    def logic():
        R.next = ~(~A & B)

    return logicbi

def orr(A, B, R):

    @always_comb
    def logic():
        R.next = A | B

    return logic

def true(A, B, R):

    @always_comb
    def logic():
        R.next = intbv(-1)[len(A)-1]

    return logic
