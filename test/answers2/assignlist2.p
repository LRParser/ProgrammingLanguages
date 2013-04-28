PROGRAM :
STMT LIST
  Assign: x :=
    5
  Assign: y :=
( 1 ( 2 nil ) )
  Assign: z :=
    Function Call: car, args:
      y
  Assign: y :=
    4
Running Program
Dump of Symbol Table
  y -> 
4
  x -> 
5
  z -> 
1
Function Table
