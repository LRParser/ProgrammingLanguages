from ../../interpreterext import *
from ../../programext import *

l1 = [1,2,3,[4,5]]
listLen = len(l1)
print("listLen is: "+str(listLen))
outerSeq = None
i = 0
while( i < listLen) :
    print("index is: "+str(i))
    val = l1[i]
    print("val is: "+str(val))
    currentNum = Number(val)
    innerSeq = Sequence(currentNum)
    if(outerSeq is not None) :
        outerSeq = Sequence(outerSeq,innerSeq)
    else :
        outerSeq = Sequence(innerSeq)
    print("Eval at loop: "+str(i))
    i = (i+1)
createdList = List(outerSeq)
#evalTo = createdList.eval(None,None,None)
#print(evalTo[0])
print(createdList.eval(None,None))
