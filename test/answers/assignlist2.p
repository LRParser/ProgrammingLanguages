Input program is: 
x := 5;
y := [1,2]

End input program
Call lexer
LexToken(IDENT,'x',1,0)
LexToken(ASSIGNOP,':=',1,2)
LexToken(NUMBER,5,1,5)
LexToken(SEMICOLON,';',1,6)
LexToken(IDENT,'y',2,8)
LexToken(ASSIGNOP,':=',2,10)
LexToken(LEFTBRACKET,'[',2,13)
LexToken(NUMBER,1,2,14)
LexToken(COMMA,',',2,15)
LexToken(NUMBER,2,2,16)
LexToken(RIGHTBRACKET,']',2,17)
Call parser
p_fact_NUMBER
p_term_fact
p_expr_term
p_element_expr
p_assn
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
PROGRAM :
STMT LIST
  Assign: x :=
    5
  Assign: y :=
      1
      2
Running Program
Dump of Symbol Table
Print List
  y -> [1, [2]] 
  x -> 5 
Function Table
