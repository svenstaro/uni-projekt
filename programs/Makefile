AS = "../assembler/assembler.py"
EMU = "../emulator/emulator.py"

SOURCES = $(wildcard *.s) $(wildcard */*.s)
OBJECTS = $(patsubst %,%.out,$(SOURCES))
all: $(OBJECTS)

%.s.out: %.s Makefile
	$(AS) $<

.PHONY: clean
clean:
	@rm -f $(OBJECTS)
