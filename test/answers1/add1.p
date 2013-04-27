PROGRAM :
STMT LIST
  DEFINE add :
    PROC ['n'] :
      STMT LIST
        Assign: i :=
          n
        Assign: s :=
          0
        WHILE
          i
        DO
          STMT LIST
            Assign: s :=
              ADD
                s
                i
            Assign: i :=
              SUB
                i
                1
        Assign: return :=
          s
  Assign: n :=
    5
  Assign: s :=
    Function Call: add, args:
      n
Running Program
Dump of Symbol Table
  s -> 15 
  n -> 5 
Function Table
  add
