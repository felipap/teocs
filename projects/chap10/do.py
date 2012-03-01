#!/usr/bin/env python3

# Compiler I: Syntax Analysis
# I'M READY FOR CODING!

from functools import reduce
from urllib.parse import quote
import sys
import os

KEYWORDS = ('class', 'constructor', 'function', 'method', 'field',
            'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
            'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return')
SYMBOLS = ('{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
            '-', '*', '/', '&', '|', '<', '>', '=',  '~')

KEYWORD = 0
SYMBOL = 1
IDENTIFIER = 2
INT_CONST = 3
STRING_CONST = 4

TYPES = {
    KEYWORD: "keyword",
	SYMBOL: "symbol",
	IDENTIFIER: "identifier",
	INT_CONST: "integerConstant",
	STRING_CONST: "stringConstant",
}

class JackTokenizer(object):
    """ JackTokenizer removes all comments and white space from the input
    stream and breaks it onto Jack language tokens, as specified by the Jack
    grammar.
    """

    _dec_file_ptr = lambda self, num: self.file.seek(self.file.tell()-num)

    def __init__(self, file):
        """ is doc really needed? pff """
        self.file = file
    
    def _group_until(self, identifier):
        """ 
        # skips the file characters until identifier is found
        # returns the whole thing
        # returns False if EOF reached
        """

        stretch = ''
        char = self.file.read(len(identifier))
        while char: # while not EOF
            if char == identifier:
                stretch += char
                return stretch
            stretch += char[0]
            self._dec_file_ptr(len(identifier)-1)
            char = self.file.read(len(identifier))
        return False

    def _group_until_logic(self, function, size=1):
        """
        # groups the file characters until function(chars) is true
        # another version of _group_until using a function
        # returns False if EOF reached
        """

        stretch = ''
        char = self.file.read(size)
        while char: # while not EOF
            if function(char):
                self._dec_file_ptr(size)
                return stretch
            stretch += char[0]
            self._dec_file_ptr(size-1)
            char = self.file.read(size)
        return False

    def hasMoreTokens(self):
        """ Do we have more tokens in the input? """
        
        saved_pointer = self.file.tell() 
        while True:
            char = self.file.read(1)
            if not char:
                return False # EOF reached
            if char.isspace():
                continue
            if char == '/':
                char2 = self.file.read(1)
                if char2 in ('*','/'): # comments ahead
                    if char2 == '*':
                        # loop until '*/'
                        self._group_until('*/')
                    elif char2 == '/':
                        # loop until '\n'
                        self._group_until('\n')
                    continue
            self.file.seek(saved_pointer)
            return True

    def advance(self):
        """ Gets the next token from the input and makes it the current token.
        This method should only be called if hasMoreTokens() is true. Initially
        there is no current token.
        The whole program advancing logic will be built upon the file buffer
        pointers. (self.file.tell() and self.file.seek(int ptr))
        """
       
        while True:
            c = self.file.read(1)
            
            if not c:
                return False # EOF reached
            if c.isspace():
                continue # skip space-like characters
            elif c == '/':
                c2 = self.file.read(1)
                if c2 in ('*','/'): # comment found
                    self._dec_file_ptr(2)
                    if c2 == '*':
                        comment = self._group_until('*/')
                    elif c2 == '/':
                        comment = self._group_until('\n')
                    print("comment: %s" % comment.strip())
                    continue
                self._dec_file_ptr(1) # no comments, put c2 back into buffer
                            
            # if character pass over this point, is part of valid token
            if c == '"': # start of a string constant
                token = '"'+self._group_until('"')
            elif c.isdigit(): # start of a number
                self._dec_file_ptr(1)
                token = self._group_until_logic(lambda c: not c.isdigit())
            elif c.isalpha(): # start of a keyword
                self._dec_file_ptr(1)
                token = self._group_until_logic(lambda char: not char.isalpha())
            else: # single length token
                token = c

            self.current_token = token
            self._setTokenType()
            return self.current_token
        raise Exception("no tokens left")


    def _setTokenType(self):
        """ Returns the type of the current token.
        may return:
            KEYWORD, 
            SYMBOL, 
            IDENTIFIER, 
            INT_CONST, 
            STRING_CONST,
        """

        checkType = {
            KEYWORD: lambda token: token in KEYWORDS,
            SYMBOL: lambda token: token in SYMBOLS,
            INT_CONST: lambda token: token.isalnum(),
            STRING_CONST: lambda token: token[0]+token[-1] == '""',
            IDENTIFIER: lambda token: token not in KEYWORDS and not
                token[0].isdigit() and reduce(lambda x, y: x and y,
                    map(lambda c: c.isdigit() or c.isalpha() or (c is '_'),
                        token))
        }

        for token_type in checkType:
            if checkType[token_type](self.current_token):
                self.token_type = token_type
                return self.token_type
        raise Exception("no types matched.", self.current_token)
        return False

class CompilationEngine(object):
    """ Effects the actual compilation output. Gets its input from a
    JackTokenizer and emits its parsed structure into an output file/stream. The
    output is generated by a series of compilexxx() routines, one for every
    syntactic element xxx of the Jack grammar. The contract between these
    routines is that each compilexxx() routine should read the syntactic
    construct xxx from the input, advance() the tokenizer exactly beyond xxx,
    and output the parsing of xxx. Thus, compilexxx() may only be called if
    indeed xxx is the next syntactic element of the input. In the first version
    of the compiler, described in Chapter 10, this module emits a structured
    printout of the code, wrapped in XML tags. In the final version of the
    compiler, described in Chapter 11, this module generates executable VM code.
    In both cases, the parsing logic and module API are exactly the same.
    """

    _get_token = lambda self: self.tokenizer.current_token
    _get_ttype = lambda self: self.tokenizer.token_type
    _get_nttype = lambda self: TYPES[self._get_ttype()]

    markTag = lambda self, xxx: self._print("<%s>" % xxx)
    unmarkTag = lambda self, xxx: self._print("</%s>" % xxx)
    _makeToken = staticmethod(lambda tag, content:
                "<{tag}> {content} </{tag}>".format(tag=tag, content=content))
 
    def _print(self, msg):
        """ prints to the desired output """
        print(msg)
        self.file.write(msg.replace("< </","lt; </")+'\n')
    
    def printToken(self):
        self._print(self._makeToken(TYPES[self._get_ttype()],
                 self._get_token()))
    
    def _process_token(self, bool_expression):
        """ processa um token, imprime o token e avança """

        assert bool_expression, 'error here: %s' % self._get_token()
        self.printToken()
        self.tokenizer.advance()

    def __init__(self, tokenizer, output):
        """ does all that crap """
        
        self.file = output
        self.tokenizer = tokenizer
    
    def run(self):
        """ starts the process """ 

        self.tokenizer.advance() # start!
        self.compileClass()
        self.file.close()

    def compileClass(self):
        """ Compiles a complete class. """

        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token

        self.markTag('class')
        processToken(getToken() == 'class')
        processToken(getTType() == IDENTIFIER) # class name
        processToken(getToken() == '{')

        # now the body :P
        while getToken() != '}':
            if getToken() in ('field', 'static'):
                self.compileClassVarDec()
            elif getToken() in ('constructor', 'method', 'function'):
                self.compileSubroutine()
            else:
                raise Exception("wtf?", getToken())

        processToken(getToken() == '}')
        self.unmarkTag('class')
        
    def compileClassVarDec(self):
        """ Compiles a static declaration or a field declaration. """

        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token
        
        processToken(getToken() in ('static', 'field'))
        processToken(getToken() in ('int', 'char', 'boolean') or getTType() ==
                    IDENTIFIER)
        
        while getToken() != ';':
            processToken(getTType() == IDENTIFIER) # var Name
            if getToken() == ',':
                processToken(True) # ',' type varName ...)
        processToken(getToken() == ';')

    def compileSubroutine(self):
        """ what else can I say? compiles a subroutine """

        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token

        self.markTag('subroutineDec')

        # subroutine type: constructor, method, function
        processToken(getToken() in ('constructor', 'method', 'function'))
        processToken(getTType() in (IDENTIFIER, KEYWORD)) # type of return
        processToken(getTType() == IDENTIFIER) # constructor Name
        processToken(getToken() == '(') # '('
        self.compileParameterList() # PARAMETER LIST
        processToken(getToken() == ')') # ')'

        # SUBROUTINE BODY
        self.markTag('subroutineBody')
        processToken(getToken() == '{') # '{'
        while getToken() in ('var',): # varDeclarations first
            self.markTag("varDec")
            self.compileVarDec()
            self.unmarkTag("varDec")
        if getToken() in ('let','if','while','do'): # statements then
            self.compileStatements()

        processToken(getToken() == '}') # '}'
        self.unmarkTag('subroutineBody')
        self.unmarkTag('subroutineDec')
    
    def compileParameterList(self):
        """ Compiles a (possibly empty) parameter list, not including the
        enclosing “()”.
        """

        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token

        self.markTag('parameterList')

        while getToken() != ')':
            # variable type
            processToken(getTType() == KEYWORD)
            # variable name
            processToken(getTType() == IDENTIFIER)
            if getToken() == ',':
                processToken(True)
        
        self.unmarkTag('parameterList')

    def compileVarDec(self):
        """ Compiles a var declaration. """

        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token
  
        processToken(getToken() == 'var')
        processToken(getTType() in (KEYWORD, IDENTIFIER)) # 'void' or variable
        while getToken() != ';':
            processToken(getTType() == IDENTIFIER) # varName
            if getToken() == ',':
                processToken(True) # ',' ...
        processToken(getToken() == ';')

    def compileStatements(self):
        """ Compiles a sequence of statements, not including the enclosing
        '{}'. """
        
        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token
        
        self.markTag('statements')
        while getToken() != '}':
            if getToken() == 'do':
                self.compileDo()
            elif getToken() == 'if':
                self.compileIf()
            elif getToken() == 'let':
                self.compileLet()
            elif getToken() == 'while':
                self.compileWhile()
            elif getToken() == 'return':
                self.compileReturn()
            else:
                raise Exception("wtf?", getToken())
        self.unmarkTag('statements')

    def compileDo(self):
        """ Compiles a do statement. """

        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token
        
        self.markTag('doStatement')
        processToken(getToken() == 'do') # 'do'
        processToken(getTType() == IDENTIFIER) # 'var'

        if getToken() == '.':
            processToken(getToken() == '.')
            processToken(getTType() == IDENTIFIER)

        processToken(getToken() == '(')
        self.compileExpressionList()
        processToken(getToken() == ')')
        processToken(getToken() == ';')
        self.unmarkTag('doStatement')

    def compileLet(self):
        """ Compiles a let statement. """

        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token
        
        self.markTag("letStatement")
        # 'let'
        processToken(getToken() == 'let')
        # varName
        processToken(getTType() == IDENTIFIER)
        if getToken() == '[':
            processToken(getToken() == '[')
            self.compileExpression()
            processToken(getToken() == ']')
        processToken(getToken() == '=')
        self.compileExpression()
        processToken(getToken() == ';')

        self.unmarkTag("letStatement")

    def compileWhile(self):
        """ Compiles a while statement. """
        
        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token
        
        self.markTag("whileStatement")

        processToken(getToken() == 'while') # 'while'
        processToken(getToken() == '(') # '('
        self.compileExpression() # expression
        processToken(getToken() == ')') # ')'
        processToken(getToken() == '{') # '}'
        self.compileStatements() # statements List
        processToken(getToken() == '}') # '}'

        self.unmarkTag("whileStatement")

    def compileReturn(self):
        """ Compiles a return statement. """

        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token

        self.markTag("returnStatement")
       
        processToken(getToken() == 'return')
        if getToken() != ';':
            self.compileExpression()
        processToken(getToken() == ';')
        
        self.unmarkTag("returnStatement")

    def compileIf(self):
        """ Compiles an if statement, possibly with a trailing else clause. """

        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token
        
        self.markTag("ifStatement")
        
        processToken(getToken() == 'if')
        processToken(getToken() == '(')
        self.compileExpression()
        processToken(getToken() == ')')
        processToken(getToken() == '{')
        self.compileStatements()
        processToken(getToken() == '}')
        
        self.unmarkTag("ifStatement")

    def compileExpression(self):
        """ Compiles an expression. """
        
        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token
        
        self.markTag("expression")
        
        self.compileTerm()
        while getToken() in ('+', '-', '*', '/', '&', '|', '<', '>', '='):
            processToken(True)
            self.compileTerm()
        
        self.unmarkTag("expression")
    
    def compileTerm(self):
        """  Compiles a term. This routine is faced with a slight difficulty
        when trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routine must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of “[“, “(“, or “.”
        suffices to distinguish between the three possibilities. Any other
        token is not part of this term and should not be advanced over. """

        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token
        
        self.markTag("term")
        
        if getTType() in (INT_CONST, STRING_CONST):
            processToken(True)
        elif getToken() in ('true', 'false', 'null', 'this'):
            processToken(True)
        elif getTType() == IDENTIFIER:
            processToken(True)
            if getToken() == '[':
                processToken(True)
                self.compileExpression()
                processToken(getToken() == ']')
            elif getToken() == '.':
                processToken(getToken() == '.')
                processToken(getTType() == IDENTIFIER)
            if getToken() == '(':
                processToken(getToken() == '(')
                self.compileExpressionList()
                processToken(getToken() == ')')
        elif getToken() == '(': # '(' expression ')'
            processToken(True)
            self.compileExpression()
            processToken(getToken() == ')')
        elif getToken() in ('-','~'): # unaryOp term
            processToken(True)
            self.compileTerm()
        else:
            raise Exception("erro: %s, %s" % (getToken(), TYPES[getTType()]))
        
        self.unmarkTag("term")

    def compileExpressionList(self):
        """ Compiles a (possibly empty) commaseparated list of expressions. """

        getToken = self._get_token
        getTType = self._get_ttype
        processToken = self._process_token
        
        self.markTag("expressionList")
        
        if not getToken() == ')':
            self.compileExpression()
        while getToken() == ',':
            processToken(True)
            self.compileExpression()
        
        self.unmarkTag("expressionList")

__usage__ = "USAGE: do.py <dirname/filename>"

def main():
    sf = open("teste.jack")
    jt = JackTokenizer(sf)
    cp = CompilationEngine(tokenizer = jt)

def work_many(path):
    valid = filter(lambda base: base.endswith('.jack'), os.listdir(path))
    for file in valid:
        work_file(os.path.join(path, file))

def work_file(file_path):
    print("#"*80+'\n'+"#"*80)
    print("now working file: %s" % file_path)
    base = open(file_path)
    out = open(os.path.splitext(file_path)[0]+'.xml', 'w')
    jt = JackTokenizer(base)
    cp = CompilationEngine(tokenizer=jt, output=out)
    cp.run()

if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print(__usage__)
        exit(1)
    entry = os.path.abspath(sys.argv[1])
    if os.path.isfile(entry):
        work_file(entry)
    elif os.path.isabs(entry):
        work_many(entry)
    else:
        print(__usage__)
        exit(1)
