define listlengthr
proc(l)
i := 0;
ll := l;
if (nullp(ll)-1)*(0-1) then
return := 1 + listlengthr(cdr(ll))
else
return := 0
fi
end;
sizetwo := listlengthr([1,2]);
a := [1,[[23]], [4,6], 6,7,8,9,0,2,2];
sizeten := listlengthr(a);
sizezero := listlengthr([])
