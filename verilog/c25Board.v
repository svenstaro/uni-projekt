
`timescale 1ns/10ps

module c25Board (
    clk,        // clock I1
    reset,      // reset I1
    // io
    buttons,    // buttons I4
    leds,       // leds O4
    // rs232
    rx,         // receive I1           
    tx,         // send O1
    // flash 32M x16
    flashWeN,   // write enable O1
    flashCsN,   // cable select O1
    flashOeN,   // output enable O1
    flashResetN,// reset O1
    flashAdvN,  // active-low address valid O1
    flashClk,   // clock O1
    flashWait,  // ??? O1
    // ssram 256 x32
    sramOeN,    // output O1
    sramCeN,    // clock enable O1
    sramWeN,    // write enable O1
    sramBeN,    // byte enable O4
    sramAdscN,  // adress controller O1
    sramClk,    // clock O1
    // flash & ssram
    flash_sramAddr, // addr O24
    flash_sramData, // data T32
    
);

input           clk;
input           resetN;
input   [3:0]   buttons;
output  [3:0]   leds;
wire    [3:0]   leds;
input           rx;
output          tx;
wire            tx;

wire            c100mhz;

wire    [15:0]  memoryaddr;
wire    [31:0]  memQ;
wire    [31:0]  memData;
wire            romrden;
wire            ramrden;
wire            ramwren;

wire    [31:0]  romOut;
wire    [31:0]  ramOut;

assign memQ = romrden ? romOut : 'bz;
assign memQ = ramrden ? ramOut : 'bz;

wire    [7:0]   fifodata;
wire    [7:0]   fifoq;
wire            fifore;
wire            fifowe;
wire            fifoempty;

processor procI (
    .clk(clk),
    .reset(resetN),
    .buttons(buttons),
    .leds(leds),
    .rx(rx),
    .tx(tx),
    .memoryaddr(memoryaddr),
    .memoryin(memQ),
    .memoryout(memData),
    .romrden(romrden),
    .ramrden(ramrden),
    .ramwren(ramwren),
    .fifodata(fifodata),
    .fifore(fifore),
    .fifowe(fifowe),
    .fifoempty(fifoempty),
    .fifofull(1'b0),
    .fifoq(fifoq)
);

ram ramI (
	.address(memoryaddr[9:0]),
	.byteena(4'h1),
	.clock(clk),
	.data(memData),
	.rden(ramrden),
	.wren(ramwren),
	.q(ramOut)
);

rom romI (
    .address(memoryaddr[7:0]),
    .clock(clk),
    .rden(romrden),
    .q(romOut)
);

fifo rsrBuffer (
    .clock(clk),
    .data(fifodata),
    .rdreq(fifore),
    .wrreq(fifowe),
    .empty(fifoempty),
    .q(fifoq)
);

disppll dpll (
        .areset(reset),
	.inclk0(clk),
	.c0(c100mhz)
);

endmodule
