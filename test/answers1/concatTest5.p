PROGRAM :
STMT LIST
  Assign: a :=
      1
        2
          3
  Assign: b :=
      4
  Assign: c :=
    CONCAT
      Function Call: cdr, args:
        a
      b
Running Program
Dump of Symbol Table
Print List
  a -> [1, [2], [[3]]] 
Print List
  c -> [[2], [[3]], 4] 
Print List
  b -> [4] 
Function Table
