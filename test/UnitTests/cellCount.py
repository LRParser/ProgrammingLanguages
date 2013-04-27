def cellCount( inputList ) :
    totalLength = 1
    for val in inputList :
        if(isinstance(val,list)) :
            totalLength = totalLength + nativeLength(val)
        else :
            totalLength = totalLength + 1
    return totalLength
