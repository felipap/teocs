// @256
// D=A
// @SP
// M=D

@START
0;JMP

(toDTrue)
	D=1
	@R15
	A=M
	0;JMP

(toDFalse)
	D=0
	@R15
	A=M
	0;JMP

(START)

// push argument 1
@ARG
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@SP
M=M-1
@THAT
D=A
@1
@0
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop that 0
@SP
M=M-1
@THAT
D=M
@0
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop that 1
@SP
M=M-1
@THAT
D=M
@1
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// push argument 0
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R14
D=M
@R13
D=D-M
@SP
A=M
M=D
@SP
M=M+1

// pop argument 0
@SP
M=M-1
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// label MAIN_LOOP_START
(FibonacciSeries.teste.MAIN_LOOP_START)

// push argument 0
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// if-goto COMPUTE_ELEMENT
@SP
M=M-1
A=M
D=M
@FibonacciSeries.teste.COMPUTE_ELEMENT
D;JNE

// goto END_PROGRAM
@FibonacciSeries.teste.END_PROGRAM
0;JMP

// label COMPUTE_ELEMENT
(FibonacciSeries.teste.COMPUTE_ELEMENT)

// push that 0
@THAT
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push that 1
@THAT
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R14
D=M
@R13
D=D+M
@SP
A=M
M=D
@SP
M=M+1

// pop that 2
@SP
M=M-1
@THAT
D=M
@2
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// push pointer 1
@THAT
D=A
@1
@0
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R14
D=M
@R13
D=D+M
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@SP
M=M-1
@THAT
D=A
@1
@0
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// push argument 0
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R14
D=M
@R13
D=D-M
@SP
A=M
M=D
@SP
M=M+1

// pop argument 0
@SP
M=M-1
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// goto MAIN_LOOP_START
@FibonacciSeries.teste.MAIN_LOOP_START
0;JMP

// label END_PROGRAM
(FibonacciSeries.teste.END_PROGRAM)

