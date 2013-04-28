PROGRAM :
STMT LIST
  Assign: a :=
( 1 ( ( 2 nil ) ( ( ( 3 nil ) nil ) nil ) ) )
  Assign: b :=
( 4 nil )
  Assign: c :=
    CONCAT
      a
      b
Running Program
Dump of Symbol Table
  a -> 
( 1 ( ( 2 nil ) ( ( ( 3 nil ) nil ) nil ) ) )
  c -> 
( ( 1 ( ( 2 nil ) ( ( ( 3 nil ) nil ) nil ) ) ) ( 4 nil ) )
  b -> 
( 4 nil )
Function Table
