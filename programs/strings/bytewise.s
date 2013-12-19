loadbyte:
ld $1, $1
lsr $1, $1, #24
ret

storebyte:
and $2, $2, #0xFF
ld $3, $1
lsr $3, $3, #8
lsl $3, $3, #8
orr $2, $3, $2
st $2, $3
ret
