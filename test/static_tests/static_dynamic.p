foo :=
    proc(x)
	    a := b + 5;
        return := a
    end;

bar :=
    proc(x)
	    b := 2;
        return := foo(0)
    end;

b := 5;
c := foo(0);
d := bar(0)
