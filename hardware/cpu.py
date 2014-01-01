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

    tState = enum('UNKNOWN', 'FETCH', 'DECODE', 'ALUOP', 'JUMP', 'LOAD', 'STORE',
                  'ADR', 'PUSH', 'POP', 'CALL', 'SWI', 'ILLEGAL', 'HALT')  # TODO add more
    state = Signal(tState.FETCH)
    substate = Signal(intbv(0)[4:])

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
        if   state == tState.UNKNOWN: # TODO mir gefällt die Lösung mit dem unknown state nicht, mal gucken, ob ich das besser hinbekomme
            if   addr[5:3] == 0b00:
                state.next  = tState.ALUOP
            elif addr[5:3] == 0b01:
                state.next  = tState.JUMP
            elif addr[5:2] == 0b100:
                state.next  = tState.LOAD
            elif addr[5:2] == 0b101:
                state.next  = tState.STORE
            elif addr[5:2] == 0b110:
                state.next  = tState.ADR
            elif addr      == 0b11100:
                state.next  = tState.PUSH
            elif addr      == 0b11101:
                state.next  = tState.POP
            elif addr      == 0b11110:
                state.next  = tState.CALL
            elif addr      == 0b11111:
                state.next  = tState.SWI
            else:
                state.next  = tState.ILLEGAL # TODO add more

        ##### FETCHING
        elif state == tState.FETCH:
            substate.next = substate + 1
            if   substate == 0:
                pcBuf.next = True
                enMAR.next = True
            elif substate == 1:
                mOe.next = True
            elif substate == 2:
                enMRR.next = True
            elif substate == 3:
                MRRbuf.next = True
                enIr.next = True
                substate.next = 0
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
            substate.next = substate + 1
            if substate == 0:
                addrBuf.next = True
                enMAR.next = True
            elif substate == 1:
                mOe.next = True
            elif substate == 2:
                enMRR.next = True
            elif substate == 3:
                MRRbuf.next = True
                enReg.next = True
                substate.next = 0
                state.next = tState.FETCH

        ##### STORING DATA INTO RAM
        elif state == tState.STORE:
            substate.next = substate + 1
            if substate == 0:
                addrymux0.next = True
                addrymux1.next = True
                ryBuf.next = True
                enMAR.next = True
            elif substate == 1:
                op2Buf.next = True # the actual value to bus
                enMDR.next = True
            elif substate == 2:
                mWe.next    = True # 1 cycle delay
            elif substate == 3:
                MDRbuf.next = True
                substate.next = 0
                state.next = tState.FETCH

        ##### ADRESS INSTR
        elif state == tState.ADR:
            enReg.next = True
            addrBuf.next = True
            state.next = tState.FETCH

        ##### PUSH
        elif state == tState.PUSH:
            substate.next = substate + 1
            if substate == 0:
                addrymux1.next = True # decrement $14 by four
                pmux.next = False # yep, false!
                enReg.next = True
                addr14Buf.next = True
            elif substate == 1:
                addrymux1.next = True # put $14 to memaddr
                ryBuf.next = True
                enMAR.next = True
            elif substate == 2:
                op2Buf.next = True
                enMDR.next = True
                mWe.next    = True # 1 cycle delay!
            elif substate == 3:
                MDRbuf.next = True
                substate.next = 0
                state.next = tState.FETCH

        ##### POP
        elif state == tState.POP:
            substate.next = substate + 1
            if substate == 0:
                addrymux1.next = True # put $14 to memaddr
                ryBuf.next = True
                enMAR.next = True
            elif substate == 1:
                mOe.next = True
            elif substate == 2:
                enMRR.next = True
            elif substate == 3:
                MRRbuf.next = True
                addrymux1.next = True
                addrymux0.next = True
                enReg.next = True
            elif substate == 4:
                addrymux1.next = True # increment $14 by 4
                pmux.next = True
                enReg.next = True
                addr14Buf.next = True
                substate.next = 0
                state.next = tState.FETCH

        ##### CALL
        elif state == tState.CALL:
            substate.next = substate + 1
            if substate == 0:
                pcBuf.next = True
                addrymux0.next = True
                enReg.next = True
            elif substate == 1:
                enCall.next = True
                enPc.next = True
                substate.next = 0
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
