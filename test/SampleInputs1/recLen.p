define listlengthr
proc(l)
currentList := l;
if (nullp(currentList)-1)*(0-1) then
return := 1 + listlengthr(cdr(currentList))
else
return := 0
fi
end;
sizetwo := listlengthr([3,4]);
a := [1,[[23]], [4,6], 6,7,8,9,0,2,2];
sizeten := listlengthr(a);
sizezero := listlengthr([])
