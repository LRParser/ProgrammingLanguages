PROGRAM :
STMT LIST
  DEFINE listlenrec :
    PROC ['lst'] :
      STMT LIST
        Assign: n :=
          Function Call: nullp, args:
            lst
        IF
          n
        THEN
          STMT LIST
            Assign: return :=
              0
        ELSE
          STMT LIST
            Assign: return :=
              ADD
                1
                Function Call: listlenrec, args:
                  Function Call: cdr, args:
                    lst
  Assign: n :=
( 1 ( 2 ( 3 nil ) ) )
  Assign: s :=
    Function Call: listlenrec, args:
      n
Running Program
Dump of Symbol Table
  s -> 
3
  n -> 
( 1 ( 2 ( 3 nil ) ) )
Function Table
  listlenrec
