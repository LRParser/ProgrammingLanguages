define listlenrec
proc( lst )
  n := nullp(lst);
  if n then return := 0 else return := 1 + listlenrec( cdr(lst) ) fi
end;
n := [1,2,3];
s := listlenrec( n )
