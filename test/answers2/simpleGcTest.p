PROGRAM :
STMT LIST
  Assign: a :=
( 1 ( 2 nil ) )
  Assign: b :=
( 3 ( 4 nil ) )
  Assign: c :=
    Function Call: car, args:
      a
  Assign: a :=
    1
  Assign: b :=
    2
Running Program
Dump of Symbol Table
  a -> 
1
  c -> 
1
  b -> 
2
Function Table
