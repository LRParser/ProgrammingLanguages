b := 5;
foo :=
    proc(x)
        return :=
            proc (y)
                return := b + 5
            end
    end;

bar :=
    proc(x)
        b := 2;
        f := foo(0);
        return := f(0)
    end;
c := foo(0);
d := bar(0);
e := c(0)
