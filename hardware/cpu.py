from myhdl import *

def cpu(clk, nextA, nextB, upcmux2, upcmux1, upcmux0, addrx15,
        rxBuf, addrBuf, aluBuf, pcBuf
        enIr, enZ, enN, enC, enV, enReg, enPC, pcmux1, pcmux0,
        enMRR, enMDR, enMAR, MRRbuf, MDRbuf, mWe, mOe):

    """
        This is a cpu state maschine. Let's see how far we come.
        All parameters are Signals as usual.

        clk (Ibool)     -- The clock
        nextA (O8)      -- next uPC addr A
        nextB (O8)      -- next uPC addr B
        upcmux2 (Obool) -- uPCMuxSelector
        upcmux1 (Obool) -- uPCMuxSelector
        upcmux0 (Obool) -- uPCMuxSelector
        addrx15 (Obool) -- set addrx for register to 15 (return addr register)
        rxBuf (Obool)   -- bufbit for xout
        addrBuf (Obool) -- bufbit for addr (pc+imm)
        aluBuf (Obool)  -- bufbit for alu
        pcBuf (Obool)   -- bufbit for pc (programcounter)
        enIr (Obool)    -- enable IR
        enZ (Obool)     -- enable zero-register
        enN (Obool)     -- enable negative-register
        enC (Obool)     -- enable carry-register
        enV (Obool)     -- enable overflow register
        enReg (Obool)   -- enable registe write
        enPC (0bool)    -- enable ProgrammCounter
        pcmux1 (Obool)  -- pcMuxSelector
        pcmux0 (Obool)  -- pcMuxSelector
        enMRR (Obool)   -- enable MemoryReadRegister
        enMDR (Obool)   -- enable MemoryDataRegister
        enMAR (Obool)   -- enable MemoryAddressRegister
        MRRbuf (Obool)  -- bufbit MemoryReadRegister
        MDRbuf (Obool)  -- bufbit MemoryDataRegister
        mWe (Obool)     -- memoryWriteEnable
        mOe (Obool)     -- memoryOutputEnable
    """

    tState = enum('RESET', 'FETCH', 'DECODE', 'EXECUTE', 'ALUOP', 'HALT') #TODO add more
    state = tState.RESET

    def logic():
        if   state == RESET:
            pass
        elif state == FETCH:
            pass
        elif state == DECODE:
            pass
        elif state == EXECUTE:
            pass
        elif state == ALUOP:
            pass
        elif state == HALT:
            pass

    return logic
