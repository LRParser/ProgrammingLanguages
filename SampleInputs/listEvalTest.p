from interpreterext import *
from programext import *

n1 = Number(1)
n2 = Number(2)
n3 = Number(3)

s3 = Sequence(n3)
s2 = Sequence(n2,s3)
s123 = Sequence(n1,s2)

newList = List(s123)
evalList = newList.eval(None,None,None)
print(evalList)
