ProgrammingLanguages
====================

Sample usage: 

python interpretext < ./SampleInputs/add.p

python interpretext < ./SampleInputs/assignList1.p

python interpretext < ./SampleInputs/assignList2.p

python interpretext < ./SampleInput/consTest.p

python interpretext < ./SampleInput/carTest.p

Using cons will append the passed atom to the existing list and make the new list and added atom eligible for GC, e.g.:

l := [1,2];
j := cons(0,l)

After interpreting these lines, j evals to [0,1,2], similar to cons in Scheme

If j is then assigned to a different variable, e.g.:

l := [1,2];
j := cons(0,l);
j := 5

Then, both the 0 and the new list returned by cons are GC'd, when GC runs
