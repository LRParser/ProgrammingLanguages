PROGRAM :
STMT LIST
  Assign: a :=
( 1 ( ( 2 nil ) ( ( ( 3 nil ) nil ) nil ) ) )
  Assign: b :=
( 4 nil )
  Assign: c :=
    CONCAT
      b
      Function Call: cdr, args:
        a
Running Program
Dump of Symbol Table
  a -> 
( 1 ( ( 2 nil ) ( ( ( 3 nil ) nil ) nil ) ) )
  c -> 
( ( 4 nil ) ( ( 2 nil ) ( ( ( 3 nil ) nil ) nil ) ) )
  b -> 
( 4 nil )
Function Table
