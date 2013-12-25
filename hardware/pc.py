from myhdl import *

def programcounter(clk, reset, enable, imm24, reg, jumpunit, cpujump, op1, out):
    """Represents the programcounter (PC)

    All parameters are Signals as usual

    clk     (Ibool) -- The clock
    reset   (Ibool) -- A resetsignal
    enable  (Ibool) -- enable the PC
    imm24   (I24)   -- The (relative) imm24 value
    reg     (I32)   -- The (absolut) register value
    jmpunit (Ibool) -- Jumpunit result
    cpujmp  (Ibool) -- Does the cpu says 'jump'?
    op1     (Ibool) -- Wheter to use the imm24 or register
    out     (O32)   -- Output

    The result will be calculated in the following way.

    cpujump, junpunit, op1, result
     c | j | o | r
    ===+===+===+===
     0 | * | * | +4
     1 | 0 | * | +4
     1 | 1 | 0 | reg
     1 | 1 | 1 | pc+imm24

    """

    data = Signal(modbv(0)[32:])

    @always_seq(clk.posedge, reset)
    def write():
        if enable:
            if (not cpujump) or (not jumpunit):
                data.next = data + 4
            else: #cpujump == jumpunit == 1
                if not op1:
                    data.next = reg
                else:
                    data.next = data + imm24 #possible because we use a modbv

    @always_comb
    def read():
        out.next = data

    return write, read
