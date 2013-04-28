PROGRAM :
STMT LIST
  DEFINE add :
    PROC ['n'] :
      STMT LIST
        Assign: l :=
( 1 nil )
        Assign: return :=
          l
  Assign: k :=
( 3 ( 4 nil ) )
  Assign: n :=
    5
  Assign: k :=
    5
  Assign: s :=
    Function Call: add, args:
      n
Running Program
Dump of Symbol Table
  k -> 
5
  s -> 
( 1 nil )
  n -> 
5
Function Table
  add
