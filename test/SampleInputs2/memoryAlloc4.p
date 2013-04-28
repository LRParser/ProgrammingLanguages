define add 
proc( n )
  l := [1,2,3,4,5,6,7,8,9,10,11];
  i := n;
  s := 0;
  while i do s := s + i;  i := i-1 od;
  return := s
end;
k := [3,4];
n := 5;
k := 5;
s := add( n )
