Input program is: 
define cons 
proc( n )
  return := [1,n]
end;
n := [5];
s := cons( n )

End input program
Call lexer
LexToken(DEFINE,'define',1,0)
LexToken(IDENT,'cons',1,7)
LexToken(PROC,'proc',2,13)
LexToken(LPAREN,'(',2,17)
LexToken(IDENT,'n',2,19)
LexToken(RPAREN,')',2,21)
LexToken(IDENT,'return',3,25)
LexToken(ASSIGNOP,':=',3,32)
LexToken(LEFTBRACKET,'[',3,35)
LexToken(NUMBER,1,3,36)
LexToken(COMMA,',',3,37)
LexToken(IDENT,'n',3,38)
LexToken(RIGHTBRACKET,']',3,39)
LexToken(END,'end',4,41)
LexToken(SEMICOLON,';',4,44)
LexToken(IDENT,'n',5,46)
LexToken(ASSIGNOP,':=',5,48)
LexToken(LEFTBRACKET,'[',5,51)
LexToken(NUMBER,5,5,52)
LexToken(RIGHTBRACKET,']',5,53)
LexToken(SEMICOLON,';',5,54)
LexToken(IDENT,'s',6,56)
LexToken(ASSIGNOP,':=',6,58)
LexToken(IDENT,'cons',6,61)
LexToken(LPAREN,'(',6,65)
LexToken(IDENT,'n',6,67)
LexToken(RPAREN,')',6,69)
Call parser
p_param_list
p_fact_NUMBER
p_term_fact
p_expr_term
p_element_expr
p_fact_IDENT
p_term_fact
p_expr_term
p_element_expr
p_sequence_element
p_sequence_element_comma_sequence
p_list_leftbracket_sequence_rightbracket
p_element_list
p_assn
p_define_stmt
p_fact_NUMBER
p_term_fact
p_expr_term
p_element_expr
p_sequence_element
p_list_leftbracket_sequence_rightbracket
p_element_list
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
  DEFINE cons :
    PROC ['n'] :
      STMT LIST
        Assign: return :=
            1
            n
  Assign: n :=
      5
  Assign: s :=
    Function Call: cons, args:
      n
Running Program
Dump of Symbol Table
Print List
  s -> [1, [List with 1 elements]] 
Print List
  n -> [5] 
Function Table
  cons
