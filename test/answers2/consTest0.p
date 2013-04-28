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
( 5 nil )
  Assign: s :=
    Function Call: newcons, args:
      n
Running Program
Dump of Symbol Table
  s -> 
( 1 ( 5 nil ) )
  n -> 
( 5 nil )
Function Table
  newcons
