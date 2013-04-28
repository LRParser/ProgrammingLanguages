l := cons(1, cons(2, cons(3, [])));
m := cons(4, cons(5, []));
n := cons(6, cons(7, cons(8, [])));
l := cons(m, cons(2, cons(3, [])));
A := cons(n, cons(m, l));
B := cons(0, cons(cdr(A), []));
C := cons(car(l), cdr(B))
