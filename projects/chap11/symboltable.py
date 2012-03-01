#!/usr/bin/env python3

from functools import reduce

class Scope(object):
    """
    implement a API for a scope.

    self.scope saves the variables.
    self.scope = {
        var_name, {'type': bar, 'kind': toast, 'index': 1/0},
        ...
    }

    in the usual code, name and type are strings and
    kind is one among 'static', 'field', 'argument', 'local'
    """

    def __init__(self, subr_name, subr_type):
        self.label = subr_name
        self.type = subr_type
        self.scope = {}

    def __repr__(self):
        return str(self.scope)

    def __getitem__(self, key):
        return self.scope[key]
    
    def __setitem__(self, key, value):
        self.scope[key] = value
    
    def __len__(self):
        return len(self.scope)

    def _get_index(self, kind):
        # returns a valid index for variable usage
        
        occurs = [self.scope[e]['index'] for e in self.scope
                    if self.scope[e]['kind'] == kind]
        
        if not occurs: # no vars of same kind yet
            if kind == 'argument':
                # methods have 'this' as implicit first argument
                if self.type == 'method':
                    return 1
            return 0
        return max(occurs)+1

    def addVar(self, var_name, var_type, var_kind):

        if var_name in self.scope:
            raise Exception("already existent entry.", self.scope)
        self.scope[var_name] = {'type': var_type, 'kind': var_kind,
                                 'index': self._get_index(var_kind)}
    
    def inScope(self, var_name):
        # checks if variable name exists in self.core

        return var_name in self.scope

    def getObject(self, var_name):
        # returns the entry of the var_name variable

        return self.scope[var_name]
    
    def countKind(self, kind):

        count = 0
        for e in self.scope:
            if self.scope[e]['kind'] == kind:
                count += 1
        return count

class VMSymbolTable(object):
    """
    implement a SymbolTable for the compiler.
    it manages multiple scope objects.

    children = {
        subr_name: scope_obj,
        ...
    }

    """

    def __init__(self, classname):
        self.classname = classname
        self._children = dict()
        self._define_parent_scope(classname)
    
    def __getitem__(self, key):
        return self._children[key]

    def _define_parent_scope(self, classname):
        self.parent = Scope('class', None)
    
    def createScope(self, subr_name, subr_type):
        scope_object = Scope(subr_name, subr_type)
        self._children[subr_name] = scope_object
    
    def scopeExists(self, subr_name):
        return subr_name in self._children

    def getScope(self, subr_name):
        return self._children[subr_name]

    def isAccessible(self, subr_name, var_name):
        
        subr_scope = self._children[subr_name]
        subr_type = subr_scope.type

        if subr_scope.inScope(var_name):
            return True
        if self.parent.inScope(var_name):
            if subr_type == 'function' and \
                        self.parent[var_name]['kind'] != 'static':
                return False
            return True
        return False
    
    def getAddress(self, subr_name, var_name):

        var_info = self.getVar(subr_name, var_name)
        pile = var_info['kind']
        return pile if pile != 'field' else 'this', var_info['index']
    
    def getVar(self, subr_name, var_name):

        subr_scope = self._children[subr_name]
        subr_type = subr_scope.type

        if subr_scope.inScope(var_name):
            return subr_scope.getObject(var_name)

        if self.parent.inScope(var_name):
            if subr_type == 'function' and \
                    self.parent[var_name]['kind'] != 'static':
                raise Exception("variable not accessible", var_name)
            else:
                return self.parent.getObject(var_name)
                
        raise Exception("variable not accessible", var_name)
