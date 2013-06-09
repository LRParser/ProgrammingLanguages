class list(init)
    Head := init;
    Car := proc() return := car(Head) end
end;

L := list([1,2]);
x := L.Car()