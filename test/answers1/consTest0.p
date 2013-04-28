PROGRAM :
STMT LIST
  DEFINE newcons :
    PROC ['n'] :
      STMT LIST
        Assign: return :=
          Function Call: cons, args:
            1
            n
  Assign: n :=
      5
  Assign: s :=
    Function Call: newcons, args:
      n
Running Program
Dump of Symbol Table
Print List
  s -> [1, 5] 
Print List
  n -> [5] 
Function Table
  newcons
