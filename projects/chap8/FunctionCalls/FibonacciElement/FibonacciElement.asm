@256
D=A
@SP
M=D

// call Sys.init 0
@Sys.init.return1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Sys.init.return1)

(toDTrue)
	D=-1
	@R15
	A=M
	0;JMP

(toDFalse)
	D=0
	@R15
	A=M
	0;JMP

// current class: Sys

// function Sys.init 0
(Sys.init)
@0
D=A
@R13
M=D
(Sys.init._func_storage_start)
@Sys.init._func_storage_end
D;JLE
@SP
M=M+1
D=D-1
@SP
A=M
M=0
@Sys.init._func_storage_start
0;JMP
(Sys.init._func_storage_end)
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0

// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Main.fibonacci 1
@Main.fibonacci.return1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci.return1)

// label WHILE
(Sys.init$WHILE)

// goto WHILE
@Sys.init$WHILE
0;JMP

// current class: Main

// function Main.fibonacci 0
(Main.fibonacci)
@0
D=A
@R13
M=D
(Main.fibonacci._func_storage_start)
@Main.fibonacci._func_storage_end
D;JLE
@SP
M=M+1
D=D-1
@SP
A=M
M=0
@Main.fibonacci._func_storage_start
0;JMP
(Main.fibonacci._func_storage_end)
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0
@0

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

// lt
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
@R13
M=D
@Main.fibonacci.goto0
D=A
@R15
M=D

@R13
D=M
@toDTrue
D;JLT
@toDFalse
0;JMP
(Main.fibonacci.goto0)
@SP
A=M
M=D
@SP
M=M+1

// if-goto IF_TRUE
@SP
M=M-1
A=M
D=M
@Main.fibonacci$IF_TRUE
D;JNE

// goto IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP

// label IF_TRUE
(Main.fibonacci$IF_TRUE)

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

// return
/// R5 <= LCL
@LCL
D=M
@R5
M=D
/// R6 <= caller return add
@R5
D=M
@5
D=D-A
A=D
D=M
@R6
M=D
/// store pop at add inside ARGs
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
/// SP = ARG+1
@ARG
D=M
@SP
M=D+1
/// restore THAT
@R5
D=M
@1
A=D-A
D=M
M=1
@THAT
M=D
/// restore THIS
@R5
D=M
@2
A=D-A
D=M
M=1
@THIS
M=D
/// restore ARG
@R5
D=M
@3
A=D-A
D=M
M=1
@ARG
M=D
/// restore LCL
@R5
D=M
@4
A=D-A
D=M
M=1
@LCL
M=D
/// jump for caller._return
@R6
A=M
0;JMP

// label IF_FALSE
(Main.fibonacci$IF_FALSE)

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

// call Main.fibonacci 1
@Main.fibonacci.return2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci.return2)

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

// call Main.fibonacci 1
@Main.fibonacci.return3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci.return3)

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

// return
/// R5 <= LCL
@LCL
D=M
@R5
M=D
/// R6 <= caller return add
@R5
D=M
@5
D=D-A
A=D
D=M
@R6
M=D
/// store pop at add inside ARGs
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
/// SP = ARG+1
@ARG
D=M
@SP
M=D+1
/// restore THAT
@R5
D=M
@1
A=D-A
D=M
M=1
@THAT
M=D
/// restore THIS
@R5
D=M
@2
A=D-A
D=M
M=1
@THIS
M=D
/// restore ARG
@R5
D=M
@3
A=D-A
D=M
M=1
@ARG
M=D
/// restore LCL
@R5
D=M
@4
A=D-A
D=M
M=1
@LCL
M=D
/// jump for caller._return
@R6
A=M
0;JMP

