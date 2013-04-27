PROGRAM :
STMT LIST
  Assign: a :=
    Function Call: cons, args:
        2
        2
        3
        2
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
Print List
  a -> [[2, 2], 3, 2] 
Print List
  c -> [10, [[2, 2], 3, 2], 1, [2, 2], 3, 2] 
Print List
  b -> [1, [2, 2], 3, 2] 
Function Table
