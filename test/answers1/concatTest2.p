PROGRAM :
STMT LIST
  Assign: a :=
      1
          2
            3
  Assign: b :=
    CONCAT
      a
        1
        2
Running Program
Dump of Symbol Table
Print List
  a -> [1, [[2]], [[[3]]]] 
Print List
  b -> [1, [[2]], [[[3]]], 1, 2] 
Function Table
