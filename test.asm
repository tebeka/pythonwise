MEM_LOC1 = 0x200 # Example of using variable

add(r0, r2, r3)
sub(r2, r4, r4)
load(r2, MEM_LOC1)
label("L1")
move(r2, r7)
jmp(L1)
