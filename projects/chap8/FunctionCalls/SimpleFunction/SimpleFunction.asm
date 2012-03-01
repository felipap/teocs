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

// current class: foo

// function SimpleFunction.test 2
(foo.SimpleFunction.test)
@2
D=A
@R13
M=D
@foo.SimpleFunction.test._func_storage_creationEND
D;JLE
(foo.SimpleFunction.test._func_storage_creation)
@SP
A=M
M=0
@SP
M=M+1
@R13
M=M-1
D=M
@foo.SimpleFunction.test._func_storage_creation
D;JGT
(foo.SimpleFunction.test._func_storage_creationEND)

// push local 0
@LCL
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

// push local 1
@LCL
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

// not
@SP
M=M-1
@SP
A=M
D=M
D=!D
@SP
A=M
M=D
@SP
M=M+1

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

// return
@LCL
D=M
@R5
M=D
@R5
D=A
@5
D=D-A
A=D
D=M
@R6
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R5
D=M
@1
A=D-A
D=M
@THAT
M=D
@R5
D=M
@2
A=D-A
D=M
@THIS
M=D
@R5
D=M
@3
A=D-A
D=M
@ARG
M=D
@R5
D=M
@4
A=D-A
D=M
@LCL
M=D
@R6
A=M
0;JMP

