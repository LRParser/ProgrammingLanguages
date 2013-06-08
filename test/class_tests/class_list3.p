class list(X)
    L := X;
    Cons := proc(x) L := cons(x,L); return := L end;
    Car := proc() return := car(L) end;
    Cdr := proc() return := cdr(L) end
end;

Q := list([]);
T := Q.Cons(3);
T := Q.Cons(2);
T := Q.Cons(1);
x := Q.Car();
M := Q.Cdr()
