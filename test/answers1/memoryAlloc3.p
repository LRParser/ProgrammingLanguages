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
Print List
  A -> [4, []] 
Print List
  x -> [6, 7, 8] 
Print List
  c -> [[6, 7, 8], [[4, []], [4, []], 2, 3]] 
Print List
  b -> [2, 3] 
Print List
  y -> [[4, []], [4, []], 2, 3] 
Function Table
