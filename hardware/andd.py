from myhdl import *

def andd(A, B, R):
    def logic():
        R.next = A & B

    return logic
