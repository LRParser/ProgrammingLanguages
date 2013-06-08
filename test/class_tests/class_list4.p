class list(X)
    L := X;
    Cons := proc(x) return := x end
end;
Q := list(3);
T := Q.Cons(3);
T := Q.Cons(2);
T := Q.Cons(1)
