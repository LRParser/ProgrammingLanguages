PROGRAM :
STMT LIST
  DEFINE listlengthr :
    PROC ['l'] :
      STMT LIST
        Assign: i :=
          0
        Assign: ll :=
          l
        IF
          MULT
            SUB
              Function Call: nullp, args:
                ll
              1
            SUB
              0
              1
        THEN
          STMT LIST
            Assign: return :=
              ADD
                1
                Function Call: listlengthr, args:
                  Function Call: cdr, args:
                    ll
        ELSE
          STMT LIST
            Assign: return :=
              0
  Assign: sizetwo :=
    Function Call: listlengthr, args:
( 1 ( 2 nil ) )
  Assign: a :=
( 1 ( ( ( 23 nil ) nil ) ( ( 4 ( 6 nil ) ) ( 6 ( 7 ( 8 ( 9 ( 0 ( 2 ( 2 nil ) ) ) ) ) ) ) ) ) )
  Assign: sizeten :=
    Function Call: listlengthr, args:
      a
  Assign: sizezero :=
    Function Call: listlengthr, args:
Running Program
Dump of Symbol Table
  sizetwo -> 
1
  a -> 
( 1 ( ( ( 23 nil ) nil ) ( ( 4 ( 6 nil ) ) ( 6 ( 7 ( 8 ( 9 ( 0 ( 2 ( 2 nil ) ) ) ) ) ) ) ) ) )
  sizezero -> 
1
  sizeten -> 
10
Function Table
  listlengthr
