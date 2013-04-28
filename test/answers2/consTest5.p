PROGRAM :
STMT LIST
  Assign: a :=
    1
  Assign: b :=
    Function Call: cons, args:
      a
( ( 3 nil ) ( 4 ( ( ( ( 5 nil ) nil ) nil ) nil ) ) )
  Assign: c :=
    CONCAT
      b
Running Program
Dump of Symbol Table
  a -> 
1
  c -> 
( nil ( nil ( ( 3 nil ) ( 4 ( ( ( ( 5 nil ) nil ) nil ) nil ) ) ) ) )
  b -> 
( nil ( ( 3 nil ) ( 4 ( ( ( ( 5 nil ) nil ) nil ) nil ) ) ) )
Function Table
