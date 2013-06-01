define add 
proc( n )
  i := n;
  s := 0;
  while i do s := s + i;  i := i-1 od;
  return := s
end;
n := 5;
t := proc( t )
    k := t;
    return := k
    end;
s := add( n );
q := t( n )
