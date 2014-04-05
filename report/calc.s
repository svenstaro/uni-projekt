; Taschenrechner

; Lese ersten Operanden
call readInt
call writeInt
mov $5, $1

; und den Zweiten
call readInt
call writeInt
mov $2, $1
mov $1, $5

; Lese Operation ein
; + - * /
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

; Ergebnis in $1
.add:
add $1, $1, $2
jmp .end

.sub:
sub $1, $1, $2
jmp .end

.mul:
mul $1, $1, $2
jmp .end

; Division in Software
.div:
call div

; Ergebnis ausgeben
; und Programm beenden.
.end:
call writeInt
halt


readInt:
; Liest eine Ganzzahl
; in dezimal ein.
mov $1, $0
; Vorzeichen in $3
mov $3, #1

rsr $2
; Minuszeichen?
cmp $2, #45
jne .readInt_loop_start
mov $3, #-1

.readInt_loop:
rsr $2
.readInt_loop_start:
; New-Line? -> Abbruch.
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
; Gibt eine Zahl
; in Hex aus.
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
mov $3, $1
mov $1, $0

; $1 = $3/$2
cmp $2, #0
jeq $15

.div_loop:
subs $3, $3, $2
jl $15
add $1, $1, #1
jmp .div_loop
