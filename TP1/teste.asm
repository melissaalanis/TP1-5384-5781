lh x2, 0(x1)
sh x2, 0(x1)
bne x22, x23, 2
add x6, x0, x2
sub x3, x6, x2
xori x4, x2, -3
addi x1, x0, 5
andi x7, x2, 3
sll x5, x6, x4
addi x2, x2, -10
or x9, x3, x4
not x10, x5
nop
neg x12, x7
mv x7, x12
