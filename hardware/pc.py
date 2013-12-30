from myhdl import *

def programcounter(clk, reset, enable, imm24, reg, cpucall, jumpunit, cpujump, op1, outs):
    """Represents the programcounter (PC)

    All parameters are Signals as usual

    clk     (Ibool) -- The clock
    reset   (Ibool) -- A resetsignal
    enable  (Ibool) -- enable the PC
    imm24   (I24)   -- The (relative) imm24 value
    reg     (I32)   -- The (absolut) register value
    cpucall (Ibool) -- Does the cpu says 'call'? (force jump)
    jmpunit (Ibool) -- Jumpunit result
    cpujmp  (Ibool) -- Does the cpu says 'jump'?
    op1     (Ibool) -- Wheter to use the imm24 or register
    out     (O32)   -- Output

    The result will be calculated in the following way.

    cpucall, cpujump, junpunit, op1, result
     c | j | u | o | r
    ===+===+===+===
     0 | 0 | * | * | +4
     0 | 1 | 0 | * | pc
     0 | 1 | 1 | 0 | reg
     0 | 1 | 1 | 1 | pc+imm24
     1 | * | * | 0 | reg
     1 | * | * | 1 | pc+imm24

    """

    data = Signal(intbv(0)[32:])

    @always_seq(clk.posedge, reset=reset)
    def write():
        if enable:
            if not (cpucall or cpujump):
                data.next = data + 4
            elif cpucall or (cpujump and jumpunit):
                if not op1:
                    data.next = reg
                else:
                    data.next = data + imm24.signed()

    @always_comb
    def read():
        outs.next = data

    return write, read
