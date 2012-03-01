#!/usr/bin/env python3

from functools import reduce

KEYWORD = 0
SYMBOL = 1
IDENTIFIER = 2
INT_CONST = 3
STRING_CONST = 4

KEYWORDS = ('class', 'constructor', 'function', 'method', 'field',
            'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
            'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return')
SYMBOLS = ('{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
            '-', '*', '/', '&', '|', '<', '>', '=',  '~')

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


