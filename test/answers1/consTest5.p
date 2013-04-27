PROGRAM :
STMT LIST
  Assign: a :=
    1
  Assign: b :=
    Function Call: cons, args:
      a
          3
        4
              5
  Assign: c :=
    CONCAT
      b
Running Program
Dump of Symbol Table
  a -> 1 
Print List
  c -> [1, [3], 4, [[[5]]]] 
Print List
  b -> [1, [3], 4, [[[5]]]] 
Function Table
