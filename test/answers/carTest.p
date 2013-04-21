Input program is: 
y := [1,2];
t := car(y)

End input program
Call lexer
LexToken(IDENT,'y',1,0)
LexToken(ASSIGNOP,':=',1,2)
LexToken(LEFTBRACKET,'[',1,5)
LexToken(NUMBER,1,1,6)
LexToken(COMMA,',',1,7)
LexToken(NUMBER,2,1,8)
LexToken(RIGHTBRACKET,']',1,9)
LexToken(SEMICOLON,';',1,10)
LexToken(IDENT,'t',2,12)
LexToken(ASSIGNOP,':=',2,14)
LexToken(IDENT,'car',2,17)
LexToken(LPAREN,'(',2,20)
LexToken(IDENT,'y',2,21)
LexToken(RPAREN,')',2,22)
Call parser
p_fact_NUMBER
p_term_fact
p_expr_term
p_element_expr
p_fact_NUMBER
p_term_fact
p_expr_term
p_element_expr
p_sequence_element
p_sequence_element_comma_sequence
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
  Assign: y :=
      1
      2
  Assign: t :=
    Function Call: car, args:
      y
Running Program
Dump of Symbol Table
Print List
  y -> [1, [2]] 
  t -> 1 
Function Table
