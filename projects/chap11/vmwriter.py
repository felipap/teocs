#!/usr/bin/env python3

GREENON = "\x1b[32m"
REDON = "\33[31m"
RESETCOLOR = "\x1b[0m"

class VMWriter(object):
    """ API to write VM code.
    the class doesn't test or verify the general input. """
    
    def _write(self, what):
        print(REDON)
        print(what)
        print(RESETCOLOR)
        self.output.write(what+'\n')
        
    write = lambda self, string: self._write(string)

    def __init__(self, output):
        """ initiates and sets output file """
        self.output = output
    
    def comment(self, comment):
        if not comment.startswith("//") or comment.startswith("/*"):
            if len(comment) < 80:
                comment = '// '+comment
            else:
                comment = '/* %s */' % comment
        self._write(comment)
    
    def close(self):
        self.output.close()

