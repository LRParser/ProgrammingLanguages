def nativeLength( inputList ) :
    totalLength = 1
    for val in inputList :
        if(isinstance(val,list)) :
            totalLength = totalLength + nativeLength(val)
        else :
            totalLength = totalLength + 1
    return totalLength

myList = [1,2,[3,4],[]]
print(nativeLength(myList))
