define callfunc
proc( func, val )
  return := func( val )
end;

define add
proc( n )
  i := n;
  s := 0;
  while i do s := s + i;  i := i-1 od;
  return := s
end;

i := 5;

final := callfunc( add, i )
