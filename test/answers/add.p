Input program is: 
define add 
proc( n )
  i := n;
  s := 0;
  while i do s := s + i;  i := i-1 od;
  return := s
end;
n := 5;
s := add( n )

End input program
Call lexer
LexToken(DEFINE,'define',1,0)
LexToken(IDENT,'add',1,7)
LexToken(PROC,'proc',2,12)
LexToken(LPAREN,'(',2,16)
LexToken(IDENT,'n',2,18)
LexToken(RPAREN,')',2,20)
LexToken(IDENT,'i',3,24)
LexToken(ASSIGNOP,':=',3,26)
LexToken(IDENT,'n',3,29)
LexToken(SEMICOLON,';',3,30)
LexToken(IDENT,'s',4,34)
LexToken(ASSIGNOP,':=',4,36)
LexToken(NUMBER,0,4,39)
LexToken(SEMICOLON,';',4,40)
LexToken(WHILE,'while',5,44)
LexToken(IDENT,'i',5,50)
LexToken(DO,'do',5,52)
LexToken(IDENT,'s',5,55)
LexToken(ASSIGNOP,':=',5,57)
LexToken(IDENT,'s',5,60)
LexToken(PLUS,'+',5,62)
LexToken(IDENT,'i',5,64)
LexToken(SEMICOLON,';',5,65)
LexToken(IDENT,'i',5,68)
LexToken(ASSIGNOP,':=',5,70)
LexToken(IDENT,'i',5,73)
LexToken(MINUS,'-',5,74)
LexToken(NUMBER,1,5,75)
LexToken(OD,'od',5,77)
LexToken(SEMICOLON,';',5,79)
LexToken(IDENT,'return',6,83)
LexToken(ASSIGNOP,':=',6,90)
LexToken(IDENT,'s',6,93)
LexToken(END,'end',7,95)
LexToken(SEMICOLON,';',7,98)
LexToken(IDENT,'n',8,100)
LexToken(ASSIGNOP,':=',8,102)
LexToken(NUMBER,5,8,105)
LexToken(SEMICOLON,';',8,106)
LexToken(IDENT,'s',9,108)
LexToken(ASSIGNOP,':=',9,110)
LexToken(IDENT,'add',9,113)
LexToken(LPAREN,'(',9,116)
LexToken(IDENT,'n',9,118)
LexToken(RPAREN,')',9,120)
Call parser
p_param_list
p_fact_IDENT
p_term_fact
p_expr_term
p_element_expr
p_assn
p_fact_NUMBER
p_term_fact
p_expr_term
p_element_expr
p_assn
p_fact_IDENT
p_term_fact
p_expr_term
p_fact_IDENT
p_term_fact
p_expr_term
p_fact_IDENT
p_term_fact
p_add
p_element_expr
p_assn
p_fact_IDENT
p_term_fact
p_expr_term
p_fact_NUMBER
p_term_fact
p_sub
p_element_expr
p_assn
p_while
p_fact_IDENT
p_term_fact
p_expr_term
p_element_expr
p_assn
p_define_stmt
p_fact_NUMBER
p_term_fact
p_expr_term
p_element_expr
p_assn
p_fact_IDENT
p_term_fact
p_expr_term
p_expr_list
p_fact_funcall
p_term_fact
p_expr_term
p_element_expr
p_assn
PROGRAM :
STMT LIST
  DEFINE add :
    PROC ['n'] :
      STMT LIST
        Assign: i :=
          n
        Assign: s :=
          0
        WHILE
          i
        DO
          STMT LIST
            Assign: s :=
              ADD
                s
                i
            Assign: i :=
              SUB
                i
                1
        Assign: return :=
          s
  Assign: n :=
    5
  Assign: s :=
    Function Call: add, args:
      n
Running Program
Dump of Symbol Table
  s -> 15 
  n -> 5 
Function Table
  add
