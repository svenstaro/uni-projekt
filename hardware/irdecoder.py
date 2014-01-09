from myhdl import *

def irdecoder(ir, aluop, dest, source, op1, op2, source2, imm24, imm16, sUp, prefix, jumpOp):
    """
        This is the IR decoder
        All inputs are Signals as usual

    ir      (I32)   -- The instruction itself
    aluop   (O4)    -- The decoded aluop
    dest    (O4)    -- The destination register
    source  (O4)    -- The first source register
    op1     (Obool) -- True if imm24 should be used, false for source2
    op2     (Obool) -- True if imm16 should be used, false for source2
    source2 (O4)    -- The second s ource register
    imm24   (O24)   -- The decoded 24bit width imm
    imm16   (O16)   -- The decoded 16bit width imm (for alu)
    sUp     (Obool) -- True if the status bit should be updated
    prefix  (O7)    -- The first five bits of the instruction
    jumpOp  (O5)    -- The ir for the jumpunit

    """

    @always_comb
    def logic():
        aluop.next   = ir[25:21]
        dest.next    = ir[29:25]
        source.next  = ir[21:17]
        op1.next     = ir[24]
        op2.next     = ir[16]
        source2.next = ir[4:0]
        imm24.next   = ir[24:0]
        imm16.next   = ir[16:0]
        sUp.next     = ir[29]
        prefix.next  = ir[32:25]
        jumpOp.next  = ir[30:25]

    return logic
