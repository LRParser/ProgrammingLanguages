define listlength
proc(l)
i := 0;
ll := l;
while (nullp(ll)-1)*(0-1) do
i := i + 1;
ll := cdr(ll)
od;
return := i
end;
sizetwo := listlength([1,2]);
a := [1,[[23]], [4,6], 6,7,8,9,0,2,2];
sizeten := listlength(a);
sizezero := listlength([])
