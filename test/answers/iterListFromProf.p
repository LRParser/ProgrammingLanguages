PROGRAM :
STMT LIST
  DEFINE listlength :
    PROC ['l'] :
      STMT LIST
        Assign: i :=
          0
        Assign: ll :=
          l
        WHILE
          MULT
            SUB
              Function Call: nullp, args:
                ll
              1
            SUB
              0
              1
        DO
          STMT LIST
            Assign: i :=
              ADD
                i
                1
            Assign: ll :=
              Function Call: cdr, args:
                ll
        Assign: return :=
          i
  Assign: sizetwo :=
    Function Call: listlength, args:
        1
        2
  Assign: a :=
      1
          23
        4
        6
      6
      7
      8
      9
      0
      2
      2
  Assign: sizeten :=
    Function Call: listlength, args:
      a
  Assign: sizezero :=
    Function Call: listlength, args:
Running Program
Dump of Symbol Table
  sizetwo -> 2 
Print List
  a -> [1, [[23]], [4, 6], 6, 7, 8, 9, 0, 2, 2] 
  sizezero -> 0 
  sizeten -> 10 
Function Table
  listlength