PROGRAM :
STMT LIST
  Assign: y :=
( 1 ( 2 nil ) )
  Assign: n :=
  Assign: a :=
    Function Call: nullp, args:
      y
  Assign: b :=
    Function Call: nullp, args:
      n
  Assign: c :=
    Function Call: nullp, args:
      3
  Assign: d :=
    Function Call: listp, args:
      y
  Assign: e :=
    Function Call: listp, args:
      3
  Assign: f :=
    Function Call: intp, args:
      y
  Assign: g :=
    Function Call: intp, args:
      3
  Assign: h :=
    Function Call: listp, args:
      n
Running Program
Dump of Symbol Table
  a -> 
0
  c -> 
0
  b -> 
1
  e -> 
0
  d -> 
1
  g -> 
1
  f -> 
0
  h -> 
1
  n -> 
  y -> 
( 1 ( 2 nil ) )
Function Table
