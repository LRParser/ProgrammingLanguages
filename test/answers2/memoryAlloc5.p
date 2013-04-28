PROGRAM :
STMT LIST
  Assign: a :=
    Function Call: cons, args:
      1
  Assign: b :=
    Function Call: cons, args:
      a
  Assign: c :=
    Function Call: cons, args:
      a
      b
  Assign: c :=
    5
Running Program
Dump of Symbol Table
  a -> 
( 1 nil )
  c -> 
5
  b -> 
( ( 1 nil ) nil )
Function Table
