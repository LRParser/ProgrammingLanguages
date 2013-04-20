#!/usr/bin/python
#
# interpreterext.py -
#               A python implementation of the mini language, with user-defined
#               functions
#
# Kurt Schmidt
# 7/07
#
# EDITOR:  cols=80, tabstop=2
#
# NOTES:
#               the display() method everybody has is just to graphically spit the
#               actual parse tree to the screen
#
#               The grammar can be found in programext.py  (probably should be here)
#
#
import sys
from programext import *
import pdb

######   LEXER   ###############################
# Note:  This is precisely the same lexer that exp1 uses.  Could've pulled
# it out to a different file.

from ply import lex

tokens = (
        'PLUS',
        'MINUS',
        'TIMES',
        'LPAREN',
        'RPAREN',
        'SEMICOLON',
        'COMMA',
        'AMP',
        'NUMBER',
        'ASSIGNOP',
        'WHILE',
        'DO',
        'OD',
        'IF',
        'THEN',
        'ELSE',
        'FI',
        'DEFINE',
        'PROC',
        'END',
        'IDENT',
        'LEFTBRACKET',
        'RIGHTBRACKET',
        'CONS',
        'CAR',
        'CDR',
        'NULLP',
        'INTP',
        'LISTP'
)

        # These are all caught in the IDENT rule, typed there.
reserved = {
                'while' : 'WHILE',
                'do'            : 'DO',
                'od'            : 'OD',
                'if'            : 'IF',
                'then'  : 'THEN',
                'else'  : 'ELSE',
                'fi'            : 'FI',
                'define': 'DEFINE',
                'proc'  : 'PROC',
                'end'           : 'END'
                }

# Now, this section.  We have a mapping, REs to token types (please note
# the t_ prefix).  They simply return the type.

        # t_ignore is special, and does just what it says.  Spaces and tabs
t_ignore = ' \t'

        # These are the simple maps
t_PLUS          = r'\+'
t_MINUS   = r'-'
t_TIMES         = r'\*'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_ASSIGNOP = r':='
t_SEMICOLON = r';'
t_COMMA         = r','
t_LEFTBRACKET = r'\['
t_RIGHTBRACKET = r'\]'
t_CONS = r'CONS'
t_CAR = r'CAR'
t_CDR = r'CDR'
t_NULLP = r'NULLP'
t_INTP = r'INTP'
t_LISTP = r'LISTP'
t_AMP = r'&'

def t_IDENT( t ):
        #r'[a-zA-Z_][a-zA-Z_0-9]*'
    r'[a-z]+'
    t.type = reserved.get( t.value, 'IDENT' )    # Check for reserved words
    return t

def t_NUMBER( t ) :
    r'[0-9]+'

            # t.value holds the string that matched.  Dynamic typing - no unions
    t.value = int( t.value )
    return t

    # These are standard little ditties:
def t_newline( t ):
    r'\n+'
    t.lexer.lineno += len( t.value )

    # Error handling rule
def t_error( t ):
    print "Illegal character '%s' on line %d" % ( t.value[0], t.lexer.lineno )
    return t
    #t.lexer.skip( 1 )

lex.lex()

#-----   LEXER (end)   -------------------------------


######   YACC   #####################################

import ply.yacc as yacc

    # create a function for each production (note the prefix)
    # The rule is given in the doc string

def p_program( p ) :
    'program : stmt_list'
    P = Program( p[1] )
    P.display()
    print 'Running Program'
    P.eval()
    P.dump()

def p_stmt_list( p ) :
    '''stmt_list : stmt SEMICOLON stmt_list
          | stmt'''
    if len( p ) == 2 :  # single stmt => new list
        p[0] = StmtList()
        p[0].insert( p[1] )
    else :  # we have a stmtList, keep adding to front
        p[3].insert( p[1] )
        p[0] = p[3]

def p_stmt( p ) :
    '''stmt : assign_stmt
                            | while_stmt
                            | if_stmt
                            | define_stmt'''
    p[0] = p[1]

# List parsing rules #
def p_list_leftbracket_sequence_rightbracket(p):
    'list : LEFTBRACKET sequence RIGHTBRACKET'
    print("p_list_leftbracket_sequence_rightbracket")
    p[0] = List(p[2])

def p_list_leftparen_rightparen(p):
    'list : LEFTBRACKET RIGHTBRACKET'
    print("p_list_leftparen_rightparen")
    p[0] = List()

def p_sequence_element_comma_sequence(p):
    'sequence : element COMMA sequence'
    print("p_sequence_element_comma_sequence")
    print(str(p[1].value)+","+str(p[3]))
    p[0] = Sequence(p[1],p[3])

def p_sequence_element(p):
    'sequence : element'
    print("p_sequence_element")
    p[0] = Sequence(p[1])

def p_element_list(p):
    'element : list'
    print("p_element_list")
    p[0] = List(p[1])

def p_element_expr(p):
    'element : expr'
    print("p_element_expr")
    p[0] = p[1]

def p_add( p ) :
    'expr : expr PLUS term'
    print("p_add")
    p[0] = Plus( p[1], p[3] )

def p_sub( p ) :
    'expr : expr MINUS term'
    print("p_sub")
    p[0] = Minus( p[1], p[3] )

def p_expr_list( p ) :
    '''expr_list : expr COMMA expr_list
                | expr'''
    print("p_expr_list")
    if len( p ) == 2 :  # single expr => new list
        p[0] = [ p[1] ]
    else :  # we have a expr_list, keep adding to front
        p[3].insert( 0, p[1] )
        p[0] = p[3]


def p_expr_term( p ) :
    'expr : term'
    print("p_expr_term")
    p[0] = p[1]

def p_mult( p ) :
    '''term : term TIMES fact'''
    print("p_mult")
    p[0] = Times( p[1], p[3] )

def p_term_fact( p ) :
    'term : fact'
    print("p_term_fact")
    p[0] = p[1]

def p_fact_NUM( p ) :
    'fact : NUMBER'
    p[0] = Number(p[1])

def p_fact_expr( p ) :
    'fact : LPAREN expr RPAREN'
    print("p_fact_expr")
    p[0] = p[2]

def p_fact_IDENT( p ) :
    'fact : IDENT'
    print("p_fact_IDENT")
    p[0] = Ident( p[1] )

def p_fact_funcall( p ) :
    'fact : func_call'
    print("p_fact_funcall")
    p[0] = p[1]

def p_assn( p ) :
    'assign_stmt : IDENT ASSIGNOP element'
    print("p_assn")
    p[0] = AssignStmt( p[1], p[3] )

def p_while( p ) :
    'while_stmt : WHILE expr DO stmt_list OD'
    print("p_while")
    p[0] = WhileStmt( p[2], p[4] )

def p_if( p ) :
    'if_stmt : IF expr THEN stmt_list ELSE stmt_list FI'
    print("p_if")
    p[0] = IfStmt( p[2], p[4], p[6] )

def p_def( p ) :
    'define_stmt : DEFINE IDENT PROC LPAREN param_list RPAREN stmt_list END'
    print("p_define_stmt")
    p[0] = DefineStmt( p[2], Proc( p[5], p[7] ))

def p_param_list( p ) :
    '''param_list : IDENT COMMA param_list
                | IDENT'''
    print("p_param_list")
    if len( p ) == 2 :  # single param => new list
        p[0] = [ p[1] ]
    else :  # we have a param_list, keep adding to front
        p[3].insert( 0, p[1] )
        p[0] = p[3]

def p_func_call( p ) :
    'func_call : IDENT LPAREN expr_list RPAREN'
    p[0] = FunCall( p[1], p[3] )


# Error rule for syntax errors
def p_error( p ):
    print "Syntax error in input!", str( p )
    sys.exit( 2 )





    # now, build the parser
yacc.yacc()


######   MAIN   #################################

def test_scanner( data ) :


    lex.input( data )

    # attempt to get that first token
    tok = lex.token()
    while tok :
        print tok
        tok = lex.token()


def test_parser( data ) :

    #data = ( '2', '232', '98237492' )
    #data = [ '2+4', '2-4', '2*37' ]
    #data.extend( [ 'x', 'foo', 'sof' ] )
    #data = '''x:=3; s:=0; while x do s := s+x ; x := x-1 od'''
    #data = '''x := 12;
    #       if x then
    #               y := 13
    #       else
    #               y := 0
    #       fi'''

    #data = 'if 5 then x := 13 else x:=0 fi'

    #data = '''
    #define sum ( i )
    #proc
    #  return := 0;
    #       while i do
    #               return := return + i;
    #               i := i - 1
    #       od
    #done;
    #x := 5;
    #sum( x )'''


    yacc.parse( data )


if __name__ == '__main__' :

    data=sys.stdin.read()
    print(data)

    print(data)
    test_scanner(data)
    print("Call parser")
    test_parser(data)
