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
      b
      Function Call: cdr, args:
        a
Running Program
Dump of Symbol Table
Print List
  a -> [1, [2], [[3]]] 
Print List
  c -> [4, [2], [[3]]] 
Print List
  b -> [4] 
Function Table
