; Calculator

call readInt
call writeInt
mov $5, $1
call readInt
call writeInt
mov $2, $1
mov $1, $5

.loop:
rsr $3
cmp $3, #43
jeq .add
cmp $3, #45
jeq .sub
cmp $3, #42
jeq .mul
cmp $3, #47
jeq .div
jmp .loop

.add:
add $1, $1, $2
jmp .end

.sub:
sub $1, $1, $2
jmp .end

.mul:
mul $1, $1, $2
jmp .end

.div:
call div


.end:
call writeInt

halt

readInt:
; Reads an integer from rs232
mov $1, $0
mov $3, #1

rsr $2
cmp $2, #45
jne .readInt_loop_start
mov $3, #-1

.readInt_loop:
rsr $2
.readInt_loop_start:
cmp $2, #0xA
jz .readInt_end
mul $1, $1, #10
sub $2, $2, #48
add $1, $1, $2
jmp .readInt_loop

.readInt_end:
mul $1, $1, $3
ret


writeInt:
; Writes an integer to rs232
rst #48
rst #120
mov $3, #8

.writeInt_loop:
ror $1, $1, #28
and $2, $1, #0xF
cmp $2, #9
jle .writeInt_num
add $2, $2, #0x27

.writeInt_num:
add $2, $2, #0x30
rst $2
subs $3, $3, #1
jnz .writeInt_loop

rst #0xa
ret


div:
; Computes division of $1 by $2
mov $3, $0
cmp $2, #0
jeq .div_end

.div_start:
cmp $2, #1
jeq $15

tst $2, #1
jnz .div_notby2
lsr $1, $1, #1
lsr $2, $2, #1
jmp .div_start

.div_notby2:
.div_loop:

lsl $4, $2, #1
.div_b_loop:
cmp $4, $2
jge .div_do
lsl $4, $4, #1
jmp .div_b_loop

.div_do:
lsr $4, $4, #1

subs $1, $1, $4
jlt .div_end
add $3, $3, $4
jmp .div_loop

.div_end:
mov $1, $3
ret
