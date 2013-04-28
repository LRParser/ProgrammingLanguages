define listlength
proc(l)
currentList := l;
index := 0;
while (nullp(currentList)-1)*(0-1) do
index := index + 1;
currentList := cdr(currentList)
od;
return := index
end;
sizetwo := listlength([3,4]);
a := [1,[[23]], [4,6], 6,7,8,9,0,2,2];
sizeten := listlength(a);
sizezero := listlength([])
