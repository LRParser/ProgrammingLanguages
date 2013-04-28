PROGRAM :
STMT LIST
  DEFINE listlength :
    PROC ['l'] :
      STMT LIST
        Assign: currentList :=
          l
        Assign: index :=
          0
        WHILE
          MULT
            SUB
              Function Call: nullp, args:
                currentList
              1
            SUB
              0
              1
        DO
          STMT LIST
            Assign: index :=
              ADD
                index
                1
            Assign: currentList :=
              Function Call: cdr, args:
                currentList
        Assign: return :=
          index
  Assign: sizetwo :=
    Function Call: listlength, args:
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
