PROGRAM :
STMT LIST
  Assign: a :=
    Function Call: cons, args:
( 2 ( 2 nil ) )
( 3 ( 2 nil ) )
  Assign: b :=
    Function Call: cons, args:
      1
      a
  Assign: c :=
    Function Call: cons, args:
      10
      Function Call: cons, args:
        a
        b
Running Program
Dump of Symbol Table
  a -> 
( ( 2 ( 2 nil ) ) ( 3 ( 2 nil ) ) )
  c -> 
( 10 ( ( ( 2 ( 2 nil ) ) ( 3 ( 2 nil ) ) ) ( 1 ( ( 2 ( 2 nil ) ) ( 3 ( 2 nil ) ) ) ) ) )
  b -> 
( 1 ( ( 2 ( 2 nil ) ) ( 3 ( 2 nil ) ) ) )
Function Table
