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

    def __init__( self, maxSize=100 ) :
        self.cellHeap = list()
        self.cellInUseCount = 0
        self.maxSize = maxSize

    def hasSpace( self ) :
        return (len(self.cellHeap)<self.maxSize)

    def add ( self, val ) :
        if(self.hasSpace()):
            print("Adding to heap: "+str(val))
            self.cellHeap.append(val)
            if(not isinstance(val,List)) :
                raise Exception("Can only add lists to heap")
            flattenedLength = val.flattenedLength(None,None,None) # No args needed since lists don't need to be able to store vars/exprs; leaving in until prof. decides if this is extra credit or not
            print("Flattened length is: "+str(flattenedLength))
            self.cellInUseCount = self.cellInUseCount + flattenedLength
            print("Cell in use count is: "+str(self.cellInUseCount))
                # Get length of list, and register at least this number of cells as being in use
                
        else :
            raise Exception('Heap is full')

    def collectGarbage(self, nt, ft, gh) :
        print("Cells in use at start of GC: "+str(self.cellInUseCount))
        for name in nt :
            val = nt[name]
            if(isinstance(val,List)) :
                print("Marking list: " + str(val) + "identified by: "+name + " so as to not be collected")
                val.mark(nt, ft, gh)

        itemsToRemove = set()
        for val in self.cellHeap :
            print("Found in heap: "+str(val))
            if(isinstance(val,List) and (not val.marked)) :
                print("Freeing unreferenced List: "+str(val))
                itemsToRemove.add(val)
            elif(isinstance(val,Number) and (not val.marked)) :
                print("Freeing unreferenced Number: "+str(val))
                itemsToRemove.add(val)

        # Sweep
        for val in itemsToRemove :
            listCellCount = val.flattenedLength(None,None,None)
            self.cellInUseCount = self.cellInUseCount - listCellCount
            self.cellHeap.remove(val)
        
        print("Cells in use at end of GC: "+str(self.cellInUseCount))

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

    def registerWithHeap(self,globalHeap) :
        globalHeap.add(self)

    def eval( self, nt, ft, gh ) :
        if(self.sequence is not None) :
            return list(self.sequence.eval(nt,ft,gh))
        else :
            return list()

    def numberIterator( self ) :
        return self.sequence.numberIterator()

    def successorLists( self, nt, ft, gh ) :
        retVal = list()
        for val in self.sequence.eval(nt,ft,gh) :
            if (isinstance(val,List)) :
                retVal.append(val)
        return retVal

    def flattenedLength( self, nt, ft, gh ) :
        iterable = self.sequence.eval(nt,ft,gh)
        return len(list(self.numberIterator()))

    # Recursively mark this list and any sub-lists as still being referenced
    def mark(self, nt, ft, gh) :
        if not (self.marked):
            # First, mark all contained cells/Numbers in list
            for nVal in self.numberIterator() :
                nVal.marked = True
            # Then mark the List/List pointer itself
            self.marked = True
            # Then mark any nested lists
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
            print(str(seq))
            yield seq.element.eval(nt,ft,gh)
            seq = seq.sequence

    def numberIterator( self ) :
        seq = self
        while(seq is not None) :
            if(isinstance(seq.element,Number)) :
                yield seq.element
            else :
                yield seq.numberIterator()
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

class Concat( Expr ) :
    '''expression for list concatenation'''

    def __init__( self, lhs, rhs ) :
        self.lhs = lhs
        self.rhs = rhs

    def eval( self, nt, ft, gh ) :
        lhsEval = self.lhs.eval(nt,ft,gh)
        rhsEval = self.rhs.eval(nt,ft,gh)
        if(not isinstance(lhsEval,List) or not isinstance(rhsEval,List)) :
            raise Exception("Both elements applied for List concatenation using || operator must be lists")
        lhsListEval = lhsEval.eval(nt,ft,gh)
        print("lhsListEval")
        print(lhsListEval)
        rhsListEval = rhsEval.eval(nt,ft,gh)
        print("rhsListEval")
        print(rhsListEval)
        extendedList = lhsListEval + rhsListEval
        print("Extended")
        print(extendedList)
        print(len(extendedList))
        return self.pythonListToList(extendedList)

    def display( self, nt, ft, depth=0 ) :
        print "%sCONCAT" % (tabstop*depth)
        self.lhs.display( nt, ft, depth+1 )
        self.rhs.display( nt, ft, depth+1 )

    def pythonListToList(self, inputList):
        listLen = len(inputList)
        
        outerSeq = None
        i = 0
        while( i < listLen) :
            print(str(i))
            val = inputList[i]
            currentElem = None
            if(isinstance(val,Number)) :
                currentElem = Number(val)
            elif(isinstance(val,List)) :
                currentElem = pythonListToList(inputList)
            innerSeq = Sequence(currentElem)
            if(outerSeq is not None) :
                outerSeq = Sequence(outerSeq,innerSeq)
            else :
                outerSeq = Sequence(innerSeq)
            i = (i+1)
        createdList = List(outerSeq)
        return createdList


class FunCall( Expr ) :
    '''stores a function call:
      - its name, and arguments'''
    
    def __init__( self, name, argList ) :
        self.name = name
        self.argList = argList
    
    def car( self, nt, ft, gh ) :
        if not(len(self.argList) == 1) :
            raise Exception("Car function requires exactly 1 argument")

        listArg = self.argList[0]
        listPassed = None
        if(isinstance(listArg,Ident)) :
            # We were passed an Ident
            listPassed = self.argList[0].eval(nt,ft, gh)
        elif(isinstance(listArg,List)) :
            # We were passed a List ojbect
            listPassed = listArg

        if not(isinstance(listPassed,List)) :
            raise Exception("Can only call car on List")
        
        # We have a parsed List object. Call eval to get a native list
        evaledList = listPassed.eval(nt,ft,gh)

        if(len(evaledList) < 1) :
            raise Exception("Can't call car on empty List")

        return evaledList[0]

    def cdr( self, nt, ft, gh ) :
        
        listArg = self.argList[0]
        listPassed = None
        if(isinstance(listArg,Ident)) :
            # We were passed an Ident
            listPassed = self.argList[0].eval(nt,ft, gh)
        elif(isinstance(listArg,List)) :
            # We were passed a List ojbect
            listPassed = listArg

        if not(isinstance(listPassed,List)) :
            raise Exception("Can only call cdr on List")

        # We have a parsed List object. Call eval to get a native list
        evaledList = listPassed.eval(nt,ft,gh)

        if(len(evaledList) < 1) :
            raise Exception("Can't call car on empty List")

        return evaledList[1:]

    def cons( self, nt, ft, gh ) :
        '''Returns a new list, with element prepended to existing list'''
        if not(len(self.argList) == 2) :
            raise Exception("Cons function requires exactly 2 arguments")

        atom = self.argList[0]
        listToAddTo = self.argList[1]

        if(isinstance(atom,Ident) or isinstance(atom,FunCall)) :
            atom = self.eval(nt,ft,gh)
       
        if(isinstance(listToAddTo,Ident) or isinstance(listToAddTo,FunCall)) :
            listToAddTo = listToAddTo.eval(nt,ft,gh)
 
        # Check if we have space to copy the passed list; if not, run GC
        sourceSeq = listToAddTo.sequence
        if(sourceSeq.sequence is not None) :
            wrapSeq = Sequence(sourceSeq.element,sourceSeq.sequence)
        else :
            wrapSeq = Sequence(sourceSeq.element)
        newSeq = Sequence(atom,wrapSeq) 
        newList = List(newSeq)
        print("Created list: "+str(newList))
        # Add the list pointer to the heap
        gh.add(newList)
        # Add the contents of list to the heap
        #for nVal in newList.numberIterator() :
            #gh.add(nVal)

        # Note: Only GC'ing creating lists for now, need to investigate what other GC scenarios exist

        return newList

    def eval( self, nt, ft, gh ) :
        if (self.name == "car") :
            return self.car(nt,ft, gh)
        elif(self.name == "cons") :
            return self.cons(nt,ft, gh)
        elif(self.name == "cdr") :
            return self.cdr(nt,ft, gh)
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
    
    def __init__( self, stmtList, heap ) :
        self.stmtList = stmtList
        self.nameTable = {}
        self.funcTable = {}
        self.globalHeap = heap
 
    def eval( self ) :
        self.stmtList.eval( self.nameTable, self.funcTable,self.globalHeap )
    
    def dump( self ) :
        print "Dump of Symbol Table"
        for k in self.nameTable :
            if(isinstance(self.nameTable[k],List)):
                print "  %s -> " % str(k)
                self.nameTable[k].display(self.nameTable,self.funcTable, 1)
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
