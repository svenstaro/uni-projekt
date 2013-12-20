from myhdl import *

def cpu(clk, nextA, nextB, upcmux2, upcmux1, upcmux0, rxBuf, addrx15, enIr, addrBuf, aluBuf, enZ, enN, enC, enV, enReg, 
        pcBuf, enPC, pcmux1, pcmux0, enMRR, enMDR, enMAR, MRRbuf, MDRbuf, mWe, mOe):

    """
        This is a cpu state maschine. Let's see how far we come.
        All parameters are Signals as usual.

        clk (Ibool)     -- The clock
        nextA (O8)      -- next uPC addr A
        nextB (O8)      -- next uPC addr B
        upcmux2 (Obool) -- uPCMuxSelector
        upcmux1 (Obool) -- uPCMuxSelector
        upsmux0 (Obool) -- uPCMuxSelector
        rxBuf (Obool)   -- bufbit for xout
        addrx15 (Obool) -- set addrx for register to 15 (return addr register)
        enIr (Obool)    -- enable IR
        addrBuf (Obool) -- bufbit for addr (pc+imm)
        aluBuf (Obool)  -- bufbit for alu
        enZ (Obool)     -- enable zero-register
        enN (Obool)     -- enable negative-register
        enC (Obool)     -- enable carry-register
        enV (Obool)     -- enable overflow register
        enReg (Obool)   -- enable registe write
        pcBuf (Obool)   -- bufbit for pc (programcounter)
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

    pass
