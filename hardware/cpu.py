# -*- coding: utf-8 -*-
from myhdl import *


def cpu(clk, reset, addr,
        addrymux1, addrymux0, pmux,
        addrBuf, op2Buf, addr14Buf, ryBuf, aluBuf, pcBuf,
        enAlu, enIr, enPc, enReg, enJump, enCall, enSup,
        enMRR, enMDR, enMAR, MRRbuf, MDRbuf, mWe, mOe):
    """
        This is a cpu state maschine. Let's see how far we come.
        All parameters are Signals as usual.

        clk       (Ibool) -- The clock
        reset     (Ireset)-- The reset signal
        addr      (I5)    -- Next action
        addrymux1 (Obool) -- mux1 for reginput
        addrymux0 (Obool) -- mux0 for reginput
        pmux      (Obool) -- if true, dx will be incremented by 4, decremented otherwise (used for push/pop)
        pcmux1    (Obool) -- pcMuxSelector
        pcmux0    (Obool) -- pcMuxSelector
        addrBuf   (Obool) -- bufbit for addr (pc+imm or reg)
        op2Buf    (Obool) -- bufbit for second opcode
        addr14Buf (Obool) -- bufbit for addr14buf
        ryBuf     (Obool) -- bufbit for content of y register
        aluBuf    (Obool) -- bufbit for alu
        pcBuf     (Obool) -- bufbit for pc (programcounter)
        enIr      (Obool) -- enable IR
        enPc      (Obool) -- enable ProgrammCounter
        enReg     (Obool) -- enable registe write
        enJump    (Obool) -- enable jumping
        enCall    (Obool) -- force jumping
        enSup     (Obool) -- enable statusUpdate
        enMRR     (Obool) -- enable MemoryReadRegister
        enMDR     (Obool) -- enable MemoryDataRegister
        enMAR     (Obool) -- enable MemoryAddressRegister
        MRRbuf    (Obool) -- bufbit MemoryReadRegister
        MDRbuf    (Obool) -- bufbit MemoryDataRegister
        mWe       (Obool) -- memoryWriteEnable
        mOe       (Obool) -- memoryOutputEnable
    """

    tState = enum('UNKNOWN',
                  'FETCH', 'FETCH2', 'FETCH3', 'FETCH4',
                  'DECODE', 'ALUOP', 'JUMP',
                  'LOAD', 'LOAD2', 'LOAD3', 'LOAD4',
                  'STORE', 'STORE2', 'STORE3', 'STORE4',
                  'ADR',
                  'PUSH', 'PUSH2', 'PUSH3', 'PUSH4',
                  'POP', 'POP2', 'POP3', 'POP4', 'POP5',
                  'CALL', 'CALL2',
                  'SWI', 'ILLEGAL', 'HALT')  # TODO add more
    state = Signal(tState.FETCH)

    @always_seq(clk.posedge, reset=reset)
    def logic():
        ##### Presetting signals!
        addrymux1.next = False
        addrymux0.next = False
        pmux.next = False
        addrBuf.next = False
        op2Buf.next = False
        addr14Buf.next = False
        ryBuf.next = False
        aluBuf.next = False
        pcBuf.next = False
        enAlu.next = False
        enIr.next = False
        enPc.next = False
        enReg.next = False
        enSup.next = False
        enJump.next = False
        enCall.next = False
        enMRR.next = False
        enMDR.next = False
        enMAR.next = False
        MRRbuf.next = False
        MDRbuf.next = False
        mWe.next = False
        mOe.next = False

        if __debug__:
            print state

        ##### UNKNOWN
        if   state == tState.UNKNOWN: #TODO mir gefällt die Lösung mit dem unknown state nicht, mal gucken, ob ich das besser hinbekomme
            if   addr[5:3] == 0b00:
                state.next = tState.ALUOP
            elif addr[5:3] == 0b01:
                state.next = tState.JUMP
            elif addr[5:2] == 0b100:
                state.next = tState.LOAD
            elif addr[5:2] == 0b101:
                state.next = tState.STORE
            elif addr[5:2] == 0b110:
                state.next = tState.ADR
            elif addr      == 0b11100:
                state.next = tState.PUSH
            elif addr      == 0b11101:
                state.next = tState.POP
            elif addr      == 0b11110:
                state.next = tState.CALL
            elif addr      == 0b11111:
                state.next = tState.SWI
            else:
                state.next = tState.ILLEGAL # TODO add more

        ##### FETCHING
        elif state == tState.FETCH:
            pcBuf.next = True
            enMAR.next = True
            state.next = tState.FETCH2
        elif state == tState.FETCH2:
            mOe.next = True
            state.next = tState.FETCH3
        elif state == tState.FETCH3:
            enMRR.next = True
            state.next = tState.FETCH4
        elif state == tState.FETCH4:
            MRRbuf.next = True
            enIr.next = True
            state.next = tState.DECODE

        ##### DECODING
        elif state == tState.DECODE:
            enPc.next  = True
            state.next = tState.UNKNOWN

        ##### ALUOP
        elif state == tState.ALUOP:
            enAlu.next = True
            aluBuf.next = True
            enReg.next  = True
            enSup.next  = True
            state.next = tState.FETCH

        ##### JUMPING
        elif state == tState.JUMP:
            enJump.next = True
            enPc.next = True
            state.next = tState.FETCH

        ##### LOADING
        elif state == tState.LOAD:
            addrBuf.next = True
            enMAR.next = True
            state.next = tState.LOAD2
        elif state.next == tState.LOAD2:
            mOe.next = True
            state.next = tState.LOAD3
        elif state == tState.LOAD3:
            enMRR.next = True
            state.next = tState.LOAD4
        elif state== tState.LOAD4:
            MRRbuf.next = True
            enReg.next = True
            state.next = tState.FETCH

        ##### STORING DATA INTO RAM
        elif state == tState.STORE:
            addrymux0.next = True
            addrymux1.next = True
            ryBuf.next = True
            enMAR.next = True
            state.next = tState.STORE2
        elif state == tState.STORE2:
            op2Buf.next = True #the actual value to bus
            enMDR.next = True
            state.next = tState.STORE3
        elif state == tState.STORE3:
            mWe.next    = True #1 cycle delay
            state.next = tState.STORE4
        elif state == tState.STORE4:
            MDRbuf.next = True
            state.next = tState.FETCH

        ##### ADRESS INSTR
        elif state == tState.ADR:
            enReg.next = True
            addrBuf.next = True
            state.next = tState.FETCH

        ##### PUSH
        elif state == tState.PUSH: #TODO Push pop is maybe incorrect
            addrymux1.next = True #decrement $14 by four
            pmux.next = False #yep, false!
            enReg.next = True
            addr14Buf.next = True
            state.next = tState.PUSH2
        elif state == tState.PUSH2:
            addrymux1.next = True #put $14 to memaddr
            ryBuf.next = True
            enMAR.next = True
            state.next = tState.PUSH3
        elif state == tState.PUSH3:
            op2Buf.next = True
            enMDR.next = True
            mWe.next    = True #1 cycle delay!
            state.next = tState.PUSH4
        elif state == tState.PUSH4:
            MDRbuf.next = True
            state.next = tState.FETCH

        ##### POP
        elif state == tState.POP:
            addrymux1.next = True #put $14 to memaddr
            ryBuf.next = True
            enMAR.next = True
            state.next = tState.POP2
        elif state == tState.POP2:
            mOe.next = True
            state.next = tState.POP3
        elif state == tState.POP3:
            enMRR.next = True
            state.next = tState.POP4
        elif state == tState.POP4:
            MRRbuf.next = True
            addrymux1.next = True
            addrymux0.next = True
            enReg.next = True
            state.next = tState.POP5
        elif state == tState.POP5:
            addrymux1.next = True #increment $14 by 4
            pmux.next = True
            enReg.next = True
            addr14Buf.next = True
            state.next = tState.FETCH

        ##### CALL
        elif state == tState.CALL:
            pcBuf.next = True
            addrymux0.next = True
            enReg.next = True
            state.next = tState.CALL2
        elif state == tState.CALL2:
            enCall.next = True
            enPc.next = True
            state.next = tState.FETCH

        ##### SWI
        elif state == tState.SWI:
            #TODO
            ryBuf.next = True
            state.next = tState.FETCH

        ##### HALT
        elif state == tState.HALT:
            pass

        ##### ILLEGAL
        else:
            assert False

    return logic
