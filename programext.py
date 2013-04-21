#!/usr/bin/python
#
# exp.py - Classes to represent underlying data structures for the grammar
#    below, for the mini-compiler.
#
# Kurt Schmidt
# 8/07
#
# DESCRIPTION:
#       Just a translation of the C++ implementation by Jeremy Johnson (see
#       programext.cpp)
#
# EDITOR: cols=80, tabstop=2
#
# NOTES
#   environment:
#       a dict
#
#       Procedure calls get their own environment, can not modify enclosing env
#
#   Grammar:
#       program: stmt_list 
#       stmt_list:  stmt ';' stmt_list 
#           |   stmt  
#       stmt:  assign_stmt 
#           |  define_stmt 
#           |  if_stmt 
#           |  while_stmt 
#       assign_stmt: IDENT ASSIGNOP expr
#       define_stmt: DEFINE IDENT PROC '(' param_list ')' stmt_list END
#       if_stmt: IF expr THEN stmt_list ELSE stmt_list FI
#       while_stmt: WHILE expr DO stmt_list OD
#       param_list: IDENT ',' param_list 
#           |      IDENT 
#       expr: expr '+' term   
#           | expr '-' term   
#           | term            
#       term: term '*' factor   
#           | factor            
#       factor:     '(' expr ')'  
#           |       NUMBER 
#           |       IDENT 
#           |       funcall 
#       funcall:  IDENT '(' expr_list ')'
#       expr_list: expr ',' expr_list 
#           |      expr 
#

import sys
import copy
import itertools
####  CONSTANTS   ################

    # the variable name used to store a proc's return value
returnSymbol = 'return'

tabstop = '  ' # 2 spaces

######   GARBAGE COLLECTION ########

class Heap :

    def __init__( self, nt, maxSize=100 ) :
        self.heap = list()
        self.nt = nt
        self.maxSize = maxSize

    def hasSpace( self ) :
        return (len(self.heap)<self.maxSize)

    def add ( self, val ) :
        if(self.hasSpace()):
            self.heap.append(val)
        else :
            raise Exception('Heap is full')

    def collectGarbage(self, nt, ft, gh) :
        for name in nt :
            val = nt[name]
            if(isinstance(val,List)) :
                print("Marking list: " + str(val) + "identified by: "+name + " so as to not be collected")
                val.mark(nt, ft, gh)
            elif(isinstance(val,Number)) :
                print("Marking number: " + str(val) + "identified by: "+name+ "so as to not be collected")
        for val in self.heap :
            if(isinstance(val,List) and (not val.marked)) :
                print("Freeing unreferenced List: "+str(val))
                self.heap.remove(val)
            elif(isinstance(val,Number) and (not val.marked)) :
                print("Freeing unreferenced Number: "+str(val))
                self.heap.remove(val)
            
######   CLASSES   ##################

class Expr :
    '''Virtual base class for expressions in the language'''

    def __init__( self ) :
        raise NotImplementedError(
            'Expr: pure virtual base class.  Do not instantiate' )

    def eval( self, nt, ft, gh ) :
        '''Given an environment and a function table, evaluates the expression,
        returns the value of the expression (an int in this grammar)'''

        raise NotImplementedError(
            'Expr.eval: virtual method.  Must be overridden.' )

    def display( self, nt, ft, depth=0 ) :
        'For debugging.'
        raise NotImplementedError(
            'Expr.display: virtual method.  Must be overridden.' )

class Element( Expr ) :
    '''Lists or integers'''
    def __init__( self, v=0 ) :
        print("Element ctor")
        self.value = v
        self.marked = False

    def eval( self, nt, ft, gh ) :
        if(isinstance(self,List)) :
            return self
        elif(isinstance(self,Number)) :
            return self.value.eval(nt,ft, gh)
        else :
            raise Exception("Element should only be a List or Number")

    def display( self, nt, ft, depth=0 ) :
        print "%s%i" % (tabstop*depth, self.value)

class Number( Element ) :
    '''Just integers'''

    def __init__( self, v=0 ) :
        self.value = v
        self.marked = False
    
    def eval( self, nt, ft, gh ) :
        return self.value

    def display( self, nt, ft, depth=0 ) :
        print "%s%i" % (tabstop*depth, self.value)

class List( Element ) :

    def __init__( self, s=None ) :
        self.sequence = s
        self.marked = False

    def display( self, nt, ft, depth=0 ) :
        if(self.sequence is not None) :
            self.sequence.display(nt,ft,depth+1)

    def addToHead( self, val ) :
        print("Adding: "+str(val))
        self.values.insert(0,val)

    def eval( self, nt, ft, gh ) :
        if(self.sequence is not None) :
            retList = list()
            for val in self.sequence.eval(nt,ft,gh) :
                print(val)
                retList.append(val)
            return retList
        else :
            return list()

    def successorLists( self, nt, ft, gh ) :
        retVal = list()
        for val in self.sequence.eval(nt,ft,gh) :
            if (isinstance(val,List)) :
                retVal.append(val)
        return retVal

    # Recursively mark this list and any sub-lists as still being referenced
    def mark(self, nt, ft, gh) :
        if not (self.marked):
            self.marked = True
            successorLists = self.successorLists(nt, ft, gh)
            if (successorLists is not None) :
                for val in successorLists:
                    if not (val.marked):
                        print("Marking successor")
                        mark(val)            

class Sequence( Expr ) :

    def __init__( self, e, s=None ) :
        self.element = e
        self.sequence = s

    def eval( self, nt, ft, gh ) :
        seq = self
        while(seq is not None) :
            yield seq.element.eval(nt,ft,gh)
            seq = seq.sequence

    def display( self, nt, ft, depth=0 ) :
        self.element.display(nt,ft,depth)
        if(self.sequence is not None):
            self.sequence.display(nt,ft,depth)

class Ident( Expr ) :
    '''Stores the symbol'''

    def __init__( self, name ) :
        self.name = name
    
    def eval( self, nt, ft, gh ) :
        return nt[ self.name ]

    def display( self, nt, ft, depth=0 ) :
        print "%s%s" % (tabstop*depth, self.name)


class Times( Expr ) :
    '''expression for binary multiplication'''

    def __init__( self, lhs, rhs ) :
        '''lhs, rhs are Expr's, the operands'''

        # test type here?
        # if type( lhs ) == type( Expr ) :
        self.lhs = lhs
        self.rhs = rhs
    
    def eval( self, nt, ft, gh ) :
        return self.lhs.eval( nt, ft, gh ) * self.rhs.eval( nt, ft, gh )

    def display( self, nt, ft, depth=0 ) :
        print "%sMULT" % (tabstop*depth)
        self.lhs.display( nt, ft, depth+1 )
        self.rhs.display( nt, ft, depth+1 )
        #print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))


class Plus( Expr ) :
    '''expression for binary addition'''

    def __init__( self, lhs, rhs ) :
        self.lhs = lhs
        self.rhs = rhs
    
    def eval( self, nt, ft, gh ) :
        return self.lhs.eval( nt, ft, gh ) + self.rhs.eval( nt, ft, gh )

    def display( self, nt, ft, depth=0 ) :
        print "%sADD" % (tabstop*depth)
        self.lhs.display( nt, ft, depth+1 )
        self.rhs.display( nt, ft, depth+1 )
        #print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))


class Minus( Expr ) :
    '''expression for binary subtraction'''

    def __init__( self, lhs, rhs ) :
        self.lhs = lhs
        self.rhs = rhs
    
    def eval( self, nt, ft, gh ) :
        return self.lhs.eval( nt, ft, gh ) - self.rhs.eval( nt, ft, gh )

    def display( self, nt, ft, depth=0 ) :
        print "%sSUB" % (tabstop*depth)
        self.lhs.display( nt, ft, depth+1 )
        self.rhs.display( nt, ft, depth+1 )
        #print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))


class FunCall( Expr ) :
    '''stores a function call:
      - its name, and arguments'''
    
    def __init__( self, name, argList ) :
        self.name = name
        self.argList = argList
    
    def car( self, nt, ft ) :
        if not(len(self.argList) == 1) :
            raise Exception("Car function requires exactly 1 argument")

        listToGetCarFrom = self.argList[0].eval(nt,ft, gh)
        
        if not(isinstance(listToGetCarFrom,List)) :
            raise Exception("Can only call car on List")

        return listToGetCarFrom.values[0].eval(nt,ft, gh)

    def cons( self, nt, ft, gh ) :
        '''Returns a new list, with element prepended to existing list'''
        if not(len(self.argList) == 2) :
            raise Exception("Cons function requires exactly 2 arguments")

        atom = self.argList[0]
        listToAddAtomTo = self.argList[1].eval(nt,ft,gh)
        print("atom is: "+str(atom))
        print("listToAddAtomTo is: "+str(listToAddAtomTo))
        
        if not(isinstance(listToAddAtomTo,List)) :
            raise Exception("Can only cons an atom onto a List")

        # Check if we have space to copy the passed list; if not, run GC
        if(gh.hasSpace()):
            copiedList = copy.copy(listToAddAtomTo)
            print("Adding to heap: "+str(copiedList))
            gh.add(copiedList)
        else :
            gh.collectGarbage(nt,ft,gh)

        # Check if we have space to add atom to from of copied list; if not, run GC
        if(gh.hasSpace()):
            print("Adding to heap: "+str(atom))
            gh.add(atom)
        # Not yet fully implemented
        else :
            gh.collectGarbage(nt,ft,gh)      

        # Shift both rightwards

        sourceSeq = listToAddAtomTo.sequence
        if(sourceSeq.sequence is not None) :
            wrapSeq = Sequence(sourceSeq.element,sourceSeq.sequence)
        else :
            wrapSeq = Sequence(sourceSeq.element)

        newSeq = Sequence(atom,wrapSeq) 
        newList = List(newSeq)
        print("Created list: ")
        print(newList.eval(nt,ft,gh))
        return newList

    def eval( self, nt, ft, gh ) :
        if (self.name == "car") :
            return self.car(nt,ft, gh)
        elif(self.name == "cons") :
            return self.cons(nt,ft, gh)
        else :
            return ft[ self.name ].apply( nt, ft, self.argList, gh )

    def display( self, nt, ft, depth=0 ) :
        print "%sFunction Call: %s, args:" % (tabstop*depth, self.name)
        for e in self.argList :
            e.display( nt, ft, depth+1 )


#-------------------------------------------------------

class Stmt :
    '''Virtual base class for statements in the language'''

    def __init__( self ) :
        raise NotImplementedError(
            'Stmt: pure virtual base class.  Do not instantiate' )

    def eval( self, nt, ft, gh ) :
        '''Given an environment and a function table, evaluates the expression,
        returns the value of the expression (an int in this grammar)'''

        raise NotImplementedError(
            'Stmt.eval: virtual method.  Must be overridden.' )

    def display( self, nt, ft, depth=0 ) :
        'For debugging.'
        raise NotImplementedError(
            'Stmt.display: virtual method.  Must be overridden.' )


class AssignStmt( Stmt ) :
    '''adds/modifies symbol in the current context'''

    def __init__( self, name, rhs ) :
        '''stores the symbol for the l-val, and the expressions which is the
        rhs'''
        self.name = name
        self.rhs = rhs
    
    def eval( self, nt, ft, gh ) :
        if(isinstance(self.rhs,List)) :
            # Lists aren't eval'd at assignment time; the values might change. Members are only evalued when we car an item off and eval it
            nt[ self.name ] = self.rhs
        else :
            nt[ self.name ] = self.rhs.eval( nt, ft, gh )

    def display( self, nt, ft, depth=0 ) :
        print "%sAssign: %s :=" % (tabstop*depth, self.name)
        self.rhs.display( nt, ft, depth+1 )


class DefineStmt( Stmt ) :
    '''Binds a proc object to a name'''

    def __init__( self, name, proc ) :
        self.name = name
        self.proc = proc

    def eval( self, nt, ft, gh ) :
        ft[ self.name ] = self.proc

    def display( self, nt, ft, depth=0 ) :
        print "%sDEFINE %s :" % (tabstop*depth, self.name)
        self.proc.display( nt, ft, depth+1 )


class IfStmt( Stmt ) :

    def __init__( self, cond, tBody, fBody ) :
        '''expects:
        cond - expression (integer)
        tBody - StmtList
        fBody - StmtList'''
        
        self.cond = cond
        self.tBody = tBody
        self.fBody = fBody

    def eval( self, nt, ft, gh ) :
        if self.cond.eval( nt, ft, gh ) > 0 :
            self.tBody.eval( nt, ft, gh )
        else :
            self.fBody.eval( nt, ft, gh )

    def display( self, nt, ft, depth=0 ) :
        print "%sIF" % (tabstop*depth)
        self.cond.display( nt, ft, depth+1 )
        print "%sTHEN" % (tabstop*depth)
        self.tBody.display( nt, ft, depth+1 )
        print "%sELSE" % (tabstop*depth)
        self.fBody.display( nt, ft, depth+1 )


class WhileStmt( Stmt ) :

    def __init__( self, cond, body ) :
        self.cond = cond
        self.body = body

    def eval( self, nt, ft, gh ) :
        while self.cond.eval( nt, ft, gh ) > 0 :
            self.body.eval( nt, ft, gh )

    def display( self, nt, ft, depth=0 ) :
        print "%sWHILE" % (tabstop*depth)
        self.cond.display( nt, ft, depth+1 )
        print "%sDO" % (tabstop*depth)
        self.body.display( nt, ft, depth+1 )

#-------------------------------------------------------

class StmtList :
    '''builds/stores a list of Stmts'''

    def __init__( self ) :
        self.sl = []
    
    def insert( self, stmt ) :
        self.sl.insert( 0, stmt )
    
    def eval( self, nt, ft, gh ) :
        for s in self.sl :
            s.eval( nt, ft, gh )
    
    def display( self, nt, ft, depth=0 ) :
        print "%sSTMT LIST" % (tabstop*depth)
        for s in self.sl :
            s.display( nt, ft, depth+1 )


class Proc :
    '''stores a procedure (formal params, and the body)

    Note that, while each function gets its own environment, we decided not to
    allow side-effects, so, no access to any outer contexts.  Thus, nesting
    functions is legal, but no different than defining them all in the global
    environment.  Further, all calls are handled the same way, regardless of
    the calling environment (after the actual args are evaluated); the proc
    doesn't need/want/get an outside environment.'''

    def __init__( self, paramList, body ) :
        '''expects a list of formal parameters (variables, as strings), and a
        StmtList'''

        self.parList = paramList
        self.body = body

    def apply( self, nt, ft, args, gh ) :
        newContext = {}

        # sanity check, # of args
        if len( args ) is not len( self.parList ) :
            print "Param count does not match:"
            sys.exit( 1 )

        # bind parameters in new name table (the only things there right now)
            # use zip, bastard
        for i in range( len( args )) :
            newContext[ self.parList[i] ] = args[i].eval( nt, ft, gh )

        # evaluate the function body using the new name table and the old (only)
        # function table.  Note that the proc's return value is stored as
        # 'return in its nametable

        self.body.eval( newContext, ft, gh )
        if newContext.has_key( returnSymbol ) :
            return newContext[ returnSymbol ]
        else :
            print "Error:  no return value"
            sys.exit( 2 )
    
    def display( self, nt, ft, depth=0 ) :
        print "%sPROC %s :" % (tabstop*depth, str(self.parList))
        self.body.display( nt, ft, depth+1 )


class Program :
    
    def __init__( self, stmtList ) :
        self.stmtList = stmtList
        self.nameTable = {}
        self.funcTable = {}
        self.globalHeap = Heap(self.nameTable,100)
 
    def eval( self ) :
        self.stmtList.eval( self.nameTable, self.funcTable,self.globalHeap )
    
    def dump( self ) :
        print "Dump of Symbol Table"
        for k in self.nameTable :
            if(isinstance(self.nameTable[k],List)):
#                print("Print List")
                print "  %s -> %s " % ( str(k), self.nameTable[k].eval(self.nameTable,self.funcTable, self.globalHeap))
            else :
                print "  %s -> %s " % ( str(k), str(self.nameTable[k]) )
        print "Function Table"
        for k in self.funcTable :
            print "  %s" % str(k)

    def display( self, depth=0 ) :
        print "%sPROGRAM :" % (tabstop*depth)
        self.stmtList.display( self.nameTable, self.funcTable )

    # A helper method that can be used to force garbage collection even before heap is full
    def collectGarbage( self ) :
        self.globalHeap.collectGarbage(self.nameTable,self.funcTable,self.globalHeap)
