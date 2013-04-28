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
import logging
import collections
# from cellCount import *


GLOBAL_NAME_TABLE = dict()
GLOBAL_FUNCTION_TABLE = dict()

logging.basicConfig(
   format = "%(levelname) -4s %(message)s",
   level = logging.DEBUG
)

log = logging.getLogger('programext')


####  CONSTANTS   ################

# the variable name used to store a proc's return value
returnSymbol = 'return'

tabstop = '  ' # 2 spaces

##### General Helper Methods ########

class MiniLangUtils :

    @staticmethod
    def pythonListToList(inputList):
        listLen = len(inputList)

        outerSeq = None
        i = 0
        while( i < listLen) :

            val = inputList[i]

            # check to see if the current element is a native python type

            if isinstance(val,int) :
                # convert to Number
                currentElem = Number(val)

            elif isinstance(val, list) :
                # convert to List
                currentElem = MiniLangUtils.pythonListToList(val)

            else :
                # it's not a native python type
                currentElem = val

            innerSeq = Sequence( currentElem)

            if(outerSeq is not None) :
                outerSeq = Sequence(outerSeq,innerSeq)
            else :
                outerSeq = Sequence(innerSeq)
            i = (i+1)

        createdList = List(outerSeq)

        return createdList

######  GARBAGE COLLECTION ##########

class ConsCell:
    def __init__(self):
        self.__car = None
        self.__cdr = None
        self.__mark = False

    @property
    def mark(self):
        return self.__mark

    @property
    def car(self):
        return self.__car

    @property
    def cdr(self):
        return self.__cdr

    @staticmethod
    def check_car( val):
        if val is None:
            pass
        elif isinstance(val, Number):
            pass
        elif isinstance(val, ConsCell):
            pass
        elif isinstance(val, Sequence):
            pass
        else:
            raise Exception("Invalid car %s" % val)

    @staticmethod
    def check_cdr(val):
        '''cdr can't end in numbers... it must be a ConsCell.  This is
        consistent with Lisp.
        '''
        if val is None:
            pass
        elif isinstance(val, ConsCell):
            pass
        elif isinstance(val, Sequence):
            pass
        else:
            raise Exception("Invalid cdr")

    @staticmethod
    def eval(cell):
        if (cell is None) or (isinstance(cell, Number)):
            yield cell
        ConsCell.eval(cell.car)
        ConsCell.eval(cell.cdr)

    @staticmethod
    def mark_cell(cell):
        if not isinstance(cell, ConsCell):
            return
        cell.mark = True
        ConsCell.mark_cell(cell.car)
        ConsCell.mark_cell(cell.cdr)

    def __to_string(self, val):
        if val is None:
            return "nil"
        elif isinstance(val, ConsCell):
            return str(val)
        else:
            return str(val)

    def __str__(self):
        return "( %s %s )" % (self.__to_string(self.car), self.__to_string(self.cdr))




class HeapCell:
    "The atomic item in the heap with some useful attributes for gc"
    def __init__(self, cell):
        self.cell = cell
        self.allocated = False


class Heap :

    def __init__( self, maxSize=100 ) :
        self.cellHeap = list()
        self.maxSize = maxSize
        self.allocated = False
        for i in range(maxSize):
            self.cellHeap.append(HeapCell(ConsCell()))

    def hasSpace( self ) :
        num_allocated = self.get_count_allocated()
        return ( num_allocated < self.maxSize)


    def is_alloc(self, cons_cell):
        for heap_cell in self.cellHeap:
            if hex(id(cons_cell)) == hex(id(heap_cell.cell)):
                return heap_cell.allocated

        return False

    def __find_available(self):
        for cell in self.cellHeap:
            if cell.allocated == False:
                cell.cell.car = None
                cell.cell.cdr = None
                cell.allocated = True
                log.debug("available cell: %s %s" % (hex(id(cell.cell)), cell.cell))
                return cell.cell

    def alloc(self):
        "retuns a ConsCell.  It may invoke GC"

        if self.hasSpace():
            log.debug("Num cells in use: %s" % self.get_count_allocated())
            return self.__find_available()
        else:
            log.debug("out of memory, collecting...")
            self.collect(GLOBAL_NAME_TABLE, GLOBAL_FUNCTION_TABLE)
            if not self.hasSpace():
                #still don't have enough memory...
                raise MemoryError("Out of memory in the heap")
            else:
                return self.__find_available()

    def get_count_allocated(self):
        return len(filter(lambda x: x.allocated == True, self.cellHeap))

    def print_cells(self):
        for cell in self.cellHeap:
            log.debug("Cell: %s is %s" % (hex(id(cell.cell)), cell.cell))

    def collect(self, nt, ft):
        num_allocated_start = self.get_count_allocated()
        log.info("Starting GC with %s used cells" % num_allocated_start)
        self.print_cells()

        for cell in self.cellHeap:
            cell.cell.mark = False

        for name in nt:
            val = BuiltIns.get_cell(nt[name])
            if isinstance(val, ConsCell):
                log.debug("Found val %s" % val)
                for cell in self.cellHeap:
                    if hex(id(cell.cell)) == hex(id(val)):
                        ConsCell.mark_cell(cell.cell)

        num_marked = len(filter(lambda x: x.cell.mark == True, self.cellHeap))
        log.info("Number of cells marked / total cells: %s / %s" % (num_marked, self.maxSize))
        #Sweep
        unmarked_list = filter(lambda x: x.cell.mark == False, self.cellHeap)
        for unmarked in unmarked_list:
            log.debug("freeing ConsCell: %s: %s" % (hex(id(unmarked.cell)), unmarked.cell))
            unmarked.allocated = False
            unmarked.cell.cell = None
            unmarked.cell.cell = None

        num_allocated_end = self.get_count_allocated()
        log.info("Number of cells now allocated: %s" % num_allocated_end)
        log.info("Freed %s cells" % (num_allocated_start -num_allocated_end) )


GLOBAL_HEAP = Heap(10)


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
        self.value = v

    def eval( self, nt, ft, gh ) :
        return self.value.eval(nt,ft, gh)

    def display( self, nt, ft, depth=0 ) :
        print "%s%i" % (tabstop*depth, self.value)

class Number( Element ) :
    '''Just integers'''

    def __init__( self, v=0 ) :
        self.marked = False
        self.value = v

    def eval( self, nt, ft, gh ) :
        return self.value

    def display( self, nt, ft, depth=0 ) :
        print "%s%i" % (tabstop*depth, self.value)

    def __str__(self):
        return "%s" % self.value

    def mark( self ) :
        self.marked = True


class List( Element ) :

    def __init__( self, s=None, cons_cell=None ) :
        if cons_cell is not None:
            self.sequence = Sequence(cons_cell=cons_cell)
        elif isinstance(s, Sequence) or s is None:
            self.sequence = s
        else:
            log.debug("s: %s" % s)
            raise TypeError

    def unPackSequence(self,seq):
        """ Loops through the sequence, pulling out
        lists and numbers and appends to one list.

        :param seq: Sequence Object.
        """

        for val in seq.values:
            # If this is a Sequence, we need to loop
            # through all of the values.
            if (isinstance(val,Sequence)):
                for y in val.values:
                    # Need to check for a nested Sequence..
                    if (isinstance(y,Sequence)):
                        self.unPackSequence(y)
                    # Check for a nested list..
                    elif (isinstance(y,List)):
                        # Append the nested list..
                        self.values.append(y)
                    else:
                        # Number object, just add to the list.
                        self.values.append(y)
            elif(isinstance(val,List)):
                # Append the nested list..
                self.values.append(val)
            else:
                # Number object, just add to the list.
                self.values.append(val)

    def eval( self, nt, ft, gh ) :
        if(self.sequence is not None) :
            return list(self.sequence.eval(nt,ft, gh))
        else :
            return list()

    def display( self, nt, ft, depth=0 ) :
        if(self.sequence is not None) :
            self.sequence.display(nt,ft,depth)

    def numberIterator( self ) :
        return self.sequence.numberIterator()



    def __str__(self):
        '''Define a repr to have pretty printing of lists.  Otherwise, we get
        the memory addr, which doesn't work out so well when trying to compare
        test results.
        '''
        return str(self.sequence)

class Sequence( Expr ) :

    def __init__( self, e=None, s=None, cons_cell=None ) :

        if cons_cell is not None:
            self.cons_cell = cons_cell
        elif s is None:
            self.cons_cell = BuiltIns.cons(e, None)
        else:
            self.cons_cell = BuiltIns.cons(e, s.cons_cell)

    def eval( self, nt=None, ft=None ) :
        return ConsCell.eval(self.cons_cell)


    def numberIterator( self ) :
        seq = self
        while(seq is not None) :
            if(isinstance(seq.element,Number)) :
                yield seq.element
            seq = seq.sequence

    def display( self, nt, ft, depth=0 ) :
        print self.cons_cell

    def __str__(self):
        return str(self.cons_cell)

class Ident( Expr ) :
    '''Stores the symbol'''

    def __init__( self, name ) :
        self.name = name


    def __str__(self):
        return self.name

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

class Plus( Expr ) :
    '''expression for binary addition'''

    def __init__( self, lhs, rhs ) :
        self.lhs = lhs
        self.rhs = rhs

    def eval( self, nt, ft, gh ) :
        print("lhs is: "+str(self.lhs))
        print("rhs is: "+str(self.rhs))
        rhsEval = self.rhs.eval(nt,ft,gh)
        while(type(rhsEval) is not int) :
            rhsEval = rhsEval.eval(nt,ft,gh)
        lhsEval = self.lhs.eval(nt,ft,gh)
        while(type(lhsEval) is not int) :
            lhsEval = lhsEval.eval(nt,ft,gh)

        print("lhsEval is: "+str(lhsEval))
        print("rhsEval is: "+str(rhsEval))
        return lhsEval + rhsEval

    def display( self, nt, ft, depth=0 ) :
        print "%sADD" % (tabstop*depth)
        self.lhs.display( nt, ft, depth+1 )
        self.rhs.display( nt, ft, depth+1 )


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


class Concat( Expr ) :
    '''expression for list concatenation'''

    def __init__( self, lhs, rhs ) :
        self.lhs = lhs
        self.rhs = rhs

    def eval( self, nt, ft, gh) :
        lhsList = self.lhs
        rhsList = self.rhs
        if(isinstance(self.lhs,Ident) or isinstance(self.lhs,FunCall)) :
            lhsList = self.lhs.eval(nt,ft,gh)

        if(isinstance(self.rhs,Ident) or isinstance(self.rhs,FunCall)) :
            rhsList = self.rhs.eval(nt,ft,gh)

        if(not isinstance(lhsList,List) or not isinstance(rhsList,List)) :
            raise Exception("Can only concat Lists")

        return List(cons_cell=BuiltIns.cons(lhsList, rhsList))



    def display( self, nt, ft, depth=0 ) :
        print "%sCONCAT" % (tabstop*depth)
        self.lhs.display( nt, ft, depth+1 )
        self.rhs.display( nt, ft, depth+1 )

class BuiltIns :

    @staticmethod
    def car(listPassed) :
        try:
            return listPassed.sequence.cons_cell.car
        except AttributeError:
            return None

    @staticmethod
    def cdr(listPassed) :
        try:
            return listPassed.sequence.cons_cell.cdr
        except AttributeError:
            return None

    @staticmethod
    def get_cell(val):
        if isinstance(val, Sequence):
            return val.cons_cell
        elif isinstance(val, List):
            return BuiltIns.get_cell(val.sequence)
        elif isinstance(val, ConsCell):
            #yeah!
            return val
        elif isinstance(val, Number):
            return val
        elif val is None:
            return None
        else:
            return None

    @staticmethod
    def cons(x, y) :
        x = BuiltIns.get_cell(x)
        y = BuiltIns.get_cell(y)

        ConsCell.check_car(x)
        ConsCell.check_cdr(y)

        #Get new cons cell
        c = GLOBAL_HEAP.alloc()

        log.debug("x: %s" % x)
        log.debug("y: %s" % y)
        #check to see if x and y are still good
        BuiltIns.check_alloc(x)
        BuiltIns.check_alloc(y)

        c.car = x
        c.cdr = y

        log.debug("New cons: %s at: %s" % (c,hex(id(c))))
        return c

    @staticmethod
    def check_alloc(element):
        if isinstance(element,ConsCell) and GLOBAL_HEAP.is_alloc(element) == False:
            raise MemoryError("Out of Memory")

class FunCall( Expr ):
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
            listPassed = listArg.eval(nt,ft, gh)
        elif(isinstance(listArg,List)) :
            # We were passed a List object
            listPassed = listArg
        elif(isinstance(listArg,FunCall)) :
            # We are getting car of the return value of a function
            listPassed = listArg.eval(nt,ft, gh)

        if not(isinstance(listPassed,List)) :
            raise Exception("Can only call car on List")

        # Validation complete
        val = BuiltIns.car(listPassed)
        if isinstance(val, ConsCell):
            return List(cons_cell=val)
        else:
            return val

    def cdr( self, nt, ft, gh):

        listArg = self.argList[0]
        listPassed = None

        if(isinstance(listArg,Ident)) :
            # We were passed an Ident
            listPassed = evalIdent(listArg, nt, ft, gh)
        elif(isinstance(listArg,FunCall)) :
            listPassed = listArg.eval(nt,ft,gh)
        elif(isinstance(listArg,List)) :
            # We were passed a List object
            listPassed = listArg

        if not(isinstance(listPassed,List)) :
            raise Exception("Can only call cdr on List")

        return List(cons_cell=BuiltIns.cdr(listPassed))


    def nullp( self, nt, ft, gh ):
        'Returns 1 if the List is Null, otherwise 0'

        the_list = self.argList[0].eval(nt,ft,gh)
        if isinstance(the_list, List):
            x = self.car(nt, ft,gh)
            if x is None:
                return 1
            else:
                return 0
        else:
            return 0
        try:
            the_list = self.argList[0].eval(nt,ft, gh).eval(nt,ft, gh);
        except:
            #It's not a list, so therefore, it's not null
            return 0;
        else:
            if not the_list:
                return 1
            else:
                return 0

    def listp( self, nt, ft, gh ):
        "Returns 1 if a list, otherwise 0"

        try:
            evaledArg = self.argList[0].eval(nt,ft, gh)
            if isinstance(evaledArg, List) or isinstance(evaledArg, list) :
                return 1
            else:
                return 0
        except:
            return 0

    def intp( self, nt, ft, gh ):
        "Returns 1 if it is Number, otherwise 0"

        try:
            if isinstance(self.argList[0], Number):
                return 1
            else:
                return 0
        except:
            return 0

    def cons( self, nt, ft, gh ) :
        '''Returns a new list, with element prepended to existing list'''

        if not(len(self.argList) == 2) :
            raise Exception("Cons function requires exactly 2 arguments")

        # evaluate the first argument
        arg1 = self.argList[0]
        destList = None
        if (isinstance(arg1, Ident) or isinstance(arg1, FunCall)):
            # needs to be evaluated twice to get to native python type
            arg1 = arg1.eval(nt, ft,gh)


        # evaluate the second argument
        arg2 = self.argList[1]
        destList = None
        if (isinstance(arg2, Ident) or isinstance(arg2, FunCall)) :
            # needs to be evaluated twice to get to the native python type
            destList = arg2.eval(nt,ft,gh)
            if isinstance(destList, int) :
                raise Exception("Can only cons an object onto a List")
        elif isinstance(arg2,List):
            destList = arg2

        return List(cons_cell=BuiltIns.cons(arg1, destList))



        newList = BuiltIns.cons(atom,destList,gh)
        return newList


    def eval( self, nt, ft, gh ) :

        func = getattr(self, self.name, None)
        # Is this function defined in this class?
        if func:
            # It is, so call it (like car, cdr, etc...)
            log.debug("Calling builtin")
            return func(nt,ft, gh)
        # Otherwise, call the function from the function table
        else :
            return ft[ self.name ].apply( nt, ft, self.argList, gh)


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

    def eval( self, nt, ft ) :
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
        print("assign: "+str(self.name)+" to: "+str(self.rhs))
        if(isinstance(self.rhs,List)) :
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

    def __init__( self, stmtList) :
        self.stmtList = stmtList
        self.nameTable = GLOBAL_NAME_TABLE
        self.funcTable = GLOBAL_FUNCTION_TABLE
        self.globalHeap = GLOBAL_HEAP

    def eval( self ) :
        self.stmtList.eval( self.nameTable, self.funcTable, self.globalHeap )

    def dump( self ) :
        print "Dump of Symbol Table"
        for k in self.nameTable :
            print "  %s -> " % ( str(k) )
            val = self.nameTable[k]
            if(isinstance(val,int)) :
                print(val)
            elif(isinstance(val,list)) :
                print(val)
            else :
                self.nameTable[k].display(self.nameTable,self.funcTable)
        print "Function Table"
        for k in self.funcTable :
            print "  %s" % str(k)

    def display( self, depth=0 ) :
        print "%sPROGRAM :" % (tabstop*depth)
        self.stmtList.display( self.nameTable, self.funcTable )

# FUNCTIONS

def evalIdent(ident, nt, ft, gh):

    orig = ident

    while (isinstance(ident, Ident) and not isinstance(ident, List)):
        ident = ident.eval(nt, ft, gh)

    if not isinstance(ident,List):
        return MiniLangUtils.pythonListToList(ident)
    else:
        return ident
