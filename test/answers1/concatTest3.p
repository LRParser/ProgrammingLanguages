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
      a
      Function Call: cons, args:
        5
        b
Running Program
Dump of Symbol Table
Print List
  a -> [1, [2], [[3]]] 
Print List
  c -> [1, [2], [[3]], 5, 4] 
Print List
  b -> [4] 
Function Table
