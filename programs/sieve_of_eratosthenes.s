jmp .start

eratosthenes:
; $1 - char[]
; $2 - int, length of array

cmp $2, #0
jz $15

push $5
push $6
push $7

; first initialize with !0
mov $3, $1
mov $4, $2

.era_init:
st $2, $3
add $3, $3, #4
subs $4, $4, #1
jnz .era_init


; main loop
; $1 - array pointer - 4
; $2 - sqr of maxvalue
; $3 - current array pointer
; $4 - current value
; $5 - array end pointer
; $6 - current value * 4
; $7 - tmp
sub $1, $1, #4

mov $4, #1
mov $6, #4

lsl $5, $2, #2
add $5, $1, $5

mov $7, #0
.era_lsr:
lsrs $2, $2, #2
add $7, $7, #1
jnz .era_lsr

mov $2, #1
lsl $2, $2, $7

.era_mainloop:
add $4, $4, #1
add $6, $6, #4

cmp $2, $4
jle .era_end

; check whether A[n] is marked
add $3, $1, $6
ld $7, $3
tst $7, $7
jz .era_mainloop


; current array pointer = A - 4 + n^2 * 4
mul $3, $4, $4
lsl $3, $3, #2
add $3, $3, $1

; cross out all multiples of n
.era_innerloop:
cmp $5, $3
jlt .era_mainloop
st $0, $3
add $3, $3, $6
jmp .era_innerloop

.era_end:
pop $7
pop $6
pop $5
ret

print_array:
; $1 - char[]
; $2 - int, length of array

cmp $2, #0
jeq $15

mov $3, $1
mov $1, #1
; $1 - counter
; $2 - max
; $3 - char*
; $4 - current value

.pr_loop:
ld $4, $3
cmp $4, #0
jz .pr_cont1
swi #1
.pr_cont1:
cmp $2, $1
add $1, $1, #1
add $3, $3, #4
jne .pr_loop
ret


.start:
mov $14, #20000
mov $1, #0
mov $2, #400
call eratosthenes
mov $1, #0
mov $2, #400
call print_array
halt
