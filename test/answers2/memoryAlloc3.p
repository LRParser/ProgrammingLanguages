PROGRAM :
STMT LIST
  Assign: c :=
    Function Call: cons, args:
  Assign: x :=
    Function Call: cons, args:
      6
      Function Call: cons, args:
        7
        Function Call: cons, args:
          8
  Assign: A :=
    Function Call: cons, args:
      4
      Function Call: cons, args:
  Assign: b :=
    Function Call: cons, args:
      2
      Function Call: cons, args:
        3
  Assign: y :=
    Function Call: cons, args:
      A
      Function Call: cons, args:
        A
        b
  Assign: c :=
    Function Call: cons, args:
      x
      Function Call: cons, args:
        y
Running Program
Dump of Symbol Table
  A -> 
( 4 ( nil nil ) )
  x -> 
( 6 ( 7 ( 8 nil ) ) )
  c -> 
( ( 6 ( 7 ( 8 nil ) ) ) ( ( ( 4 ( nil nil ) ) ( ( 4 ( nil nil ) ) ( 2 ( 3 nil ) ) ) ) nil ) )
  b -> 
( 2 ( 3 nil ) )
  y -> 
( ( 4 ( nil nil ) ) ( ( 4 ( nil nil ) ) ( 2 ( 3 nil ) ) ) )
Function Table
