define add 
proc( n )
  i := n;
  s := 0;
  while i do s := s + i;  i := i-1 od;
  return := s
end;
n := 3;
s := add( n );
l := [1,2];
j := cons(s,l)
