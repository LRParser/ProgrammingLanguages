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
  Assign: A :=
    Function Call: cons, args:
      n
      Function Call: cons, args:
        m
        l
  Assign: B :=
    Function Call: cons, args:
      0
      Function Call: cons, args:
        Function Call: cdr, args:
          A
  Assign: C :=
    Function Call: cons, args:
      Function Call: car, args:
        l
      Function Call: cdr, args:
        B
Running Program
Dump of Symbol Table
Print List
  A -> [[6, 7, 8], [4, 5], [4, 5], 2, 3] 
Print List
  C -> [[4, 5], [[4, 5], [4, 5], 2, 3]] 
Print List
  B -> [0, [[4, 5], [4, 5], 2, 3]] 
Print List
  m -> [4, 5] 
Print List
  l -> [[4, 5], 2, 3] 
Print List
  n -> [6, 7, 8] 
Function Table
