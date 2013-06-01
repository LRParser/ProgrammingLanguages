addOne := proc(x)return := x+1 end;
addTwo := proc(x)return := x+2 end;
addThree := proc(x)return := x+3 end;
addFour := proc(x)return := x+4 end;
addFive := proc(x)return := x+5 end;

square := proc(x)return := x*x end;
cube := proc(x)return := x*x*x end;
n := square(cube(2));
x := addFive(addFour(addThree(addTwo(addOne(0)))))