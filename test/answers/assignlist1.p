Input program is: 
x := (1 +2)

End input program
Call lexer
LexToken(IDENT,'x',1,0)
LexToken(ASSIGNOP,':=',1,2)
LexToken(LPAREN,'(',1,5)
LexToken(NUMBER,1,1,6)
LexToken(PLUS,'+',1,8)
LexToken(NUMBER,2,1,9)
LexToken(RPAREN,')',1,10)
Call parser
p_fact_NUMBER
p_term_fact
p_expr_term
p_fact_NUMBER
p_term_fact
p_add
p_fact_expr
p_term_fact
p_expr_term
p_element_expr
p_assn
PROGRAM :
STMT LIST
  Assign: x :=
    ADD
      1
      2
Running Program
Dump of Symbol Table
  x -> 3 
Function Table
