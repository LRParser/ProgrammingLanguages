PROGRAM :
STMT LIST
  DEFINE add :
    PROC ['n'] :
      STMT LIST
        Assign: l :=
( 1 ( 2 ( 3 ( 4 ( 5 ( 6 ( 7 ( 8 ( 9 ( 10 ( 11 nil ) ) ) ) ) ) ) ) ) ) )
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
  Assign: k :=
( 3 ( 4 nil ) )
  Assign: n :=
    5
  Assign: k :=
    5
  Assign: s :=
    Function Call: add, args:
      n
Running Program
Dump of Symbol Table
  k -> 
5
  s -> 
15
  n -> 
5
Function Table
  add
