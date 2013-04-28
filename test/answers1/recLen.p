PROGRAM :
STMT LIST
  DEFINE listlengthr :
    PROC ['l'] :
      STMT LIST
        Assign: currentList :=
          l
        IF
          MULT
            SUB
              Function Call: nullp, args:
                currentList
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
                    currentList
        ELSE
          STMT LIST
            Assign: return :=
              0
  Assign: sizetwo :=
    Function Call: listlengthr, args:
        3
        4
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
    Function Call: listlengthr, args:
      a
  Assign: sizezero :=
    Function Call: listlengthr, args:
Running Program
Dump of Symbol Table
  sizetwo -> 2 
Print List
  a -> [1, [[23]], [4, 6], 6, 7, 8, 9, 0, 2, 2] 
  sizezero -> 0 
  sizeten -> 10 
Function Table
  listlengthr
