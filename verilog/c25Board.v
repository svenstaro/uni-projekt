
`timescale 1ns/10ps

module c25Board (
    clk, reset,
    buttons, leds,
    rx, tx
);

input           clk;
input           reset;
input   [3:0]   buttons;
output  [3:0]   leds;
wire    [3:0]   leds;
input           rx;
output          tx;
wire            tx;

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
    .reset(reset),
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

endmodule
