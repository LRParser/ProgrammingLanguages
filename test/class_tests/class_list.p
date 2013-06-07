class list(init)
    L := init;
    Car := proc() return := car(L) end
end;

L := list([1,2]);
x := L.Car()