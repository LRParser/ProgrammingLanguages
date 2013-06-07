class list(init)
    L := init;
    Cons := proc(x) L := cons(x,L); return := L end;
    Car := proc() return := car(L) end;
    Cdr := proc() return := cdr(L) end
end;

L := list([]);
T := L.Cons(3);
T := L.Cons(2);
T := L.Cons(1);
x := L.Car();
M := L.Cdr()