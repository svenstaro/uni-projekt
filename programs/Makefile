AS = "../assembler/assembler.py"
DIS = "../assembler/disassembler.py"
EMU = "../emulator/emulator.py"

SOURCES = $(wildcard *.s) $(wildcard */*.s)
OBJECTS = $(patsubst %,%.out,$(SOURCES))
all: objects

objects: $(OBJECTS)
debug: $(patsubst %,%.dbg,$(OBJECTS))
dec: $(patsubst %,%.dec,$(OBJECTS))

%.s.out: %.s Makefile
	$(AS) $<

%.s.out.dbg: %.s Makefile
	$(AS) -d $<

%.s.out.dec: %.s.out Makefile
	$(DIS) $<

.PHONY: clean
clean:
	@rm -f $(OBJECTS) $(patsubst %,%.dec,$(OBJECTS)) $(patsubst %,%.dbg,$(OBJECTS))
