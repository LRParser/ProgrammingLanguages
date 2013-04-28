PROGRAM :
STMT LIST
  Assign: l :=
    Function Call: cons, args:
      1
      Function Call: cons, args:
        2
        Function Call: cons, args:
          3
  Assign: m :=
    Function Call: cons, args:
      4
      Function Call: cons, args:
        5
  Assign: n :=
    Function Call: cons, args:
      6
      Function Call: cons, args:
        7
        Function Call: cons, args:
          8
  Assign: l :=
    Function Call: cons, args:
      m
      Function Call: cons, args:
        2
        Function Call: cons, args:
          3
  Assign: m :=
    0
  Assign: n :=
    0
  Assign: n :=
    Function Call: cons, args:
      1
Running Program
Dump of Symbol Table
  m -> 0 
Print List
  l -> [[4, 5], 2, 3] 
Print List
  n -> [1] 
Function Table
