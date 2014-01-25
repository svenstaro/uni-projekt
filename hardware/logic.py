from myhdl import *

__all__ = ['identity', 'negation',
           'false', 'nor', 'xB', 'nA', 'xA', 'nB', 'xor', 'nand', 'andd', 'xnor', 'aA', 'impl', 'aB', 'xnB', 'orr', 'true']

#unary funtction
def identity(A, R):

    @always_comb
    def logic():
        R.next = A

    return logic

def negation(A, R):

    @always_comb
    def logic():
        R.next = not A

    return logic


#binary function

def false(A, B, R):

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

def aA(A, B, R):

    @always_comb
    def logic():
        R.next = A

    return logic

def impl(A, B, R):

    @always_comb
    def logic():
        R.next = ~A | B

    return logic

def aB(A, B, R):

    @always_comb
    def logic():
        R.next = B

    return logic

def xnB(A, B, R):

    @always_comb
    def logic():
        R.next = ~(~A & B)

    return logic

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
