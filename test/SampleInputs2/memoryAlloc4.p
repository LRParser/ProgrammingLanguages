define add 
proc( n )
  l := [1,2];
  i := n;
  s := 0;
  while i do s := s + i;  i := i-1 od;
  return := s
end;
k := [3,4];
n := 5;
s := add( n )
