makeadder :=
    proc(x)
        return :=
            proc(y)
                return := x+y
            end
    end;
addone := makeadder(1);
x := 2;
y := addone(1)