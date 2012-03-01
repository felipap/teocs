// fill.asm
// screen mem starts at 16384
    @LOOP
    0;JMP

(FILL)
    @R0
    M=-1
    @ITER
    0;JMP

(CLEAR)
    @R0
    M=0
    @ITER
    0;JMP

(ITER) // value to be written into word is at @R0
    
    
    @R0
    D=M
    // modify word with value at D
    @actual
    A=M
    M=D
    // next word
    @actual
    M=M+1
    // check overflow
    @24576
    D=A // maximum address
    @actual
    D=D-M // addresses left
    // iterate again or no
    @LOOP
    D;JLE
    @ITER
    0;JMP

(LOOP)
    @SCREEN
    D=A
    @actual // updates the actual pixel to 0
    M=D
    
    @KBD
    D=M
    // D now is the keyboard value
    @FILL
    D;JNE // if D != 0
    @CLEAR
    D;JGE // if D == 0
    //
