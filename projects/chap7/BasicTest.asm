@256
D=A
@SP
M=D
@500
D=A
@LCL
M=D
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

// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 3
@3
D=A
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

// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop local 0
@SP
M=M-1
@LCL
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

// pop local 1
@SP
M=M-1
@LCL
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

// pop local 2
@SP
M=M-1
@LCL
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

// pop local 3
@SP
M=M-1
@LCL
D=M
@3
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// pop local 4
@SP
M=M-1
@LCL
D=M
@4
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

