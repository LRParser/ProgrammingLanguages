from programext import *

class Heap :

    def __init__( self, maxSize=100 ) :
        self.cellHeap = list()
        self.cellInUseCount = 0
        self.maxSize = maxSize

    def hasSpace( self ) :
        return (len(self.cellHeap)<self.maxSize)

    def add ( self, val ) :
        if(self.hasSpace()):
            print("Adding to heap: "+str(val))
            self.cellHeap.append(val)
            if(not isinstance(val,List)) :
                raise Exception("Can only add lists to heap")
            flattenedLength = val.flattenedLength(None,None,None) # No args needed since lists don't need to be able to store vars/exprs; leaving in until prof. decides if this is extra credit or not
            print("Flattened length is: "+str(flattenedLength))
            self.cellInUseCount = self.cellInUseCount + flattenedLength
            print("Cell in use count is: "+str(self.cellInUseCount))
                # Get length of list, and register at least this number of cells as being in use

        else :
            raise Exception('Heap is full')

    def collectGarbage(self, nt, ft, gh) :
        print("Cells in use at start of GC: "+str(self.cellInUseCount))
        for name in nt :
            val = nt[name]
            if(isinstance(val,List)) :
                print("Marking list: " + str(val) + "identified by: "+name + " so as to not be collected")
                val.mark(nt, ft, gh)

        itemsToRemove = set()
        for val in self.cellHeap :
            print("Found in heap: "+str(val))
            if(isinstance(val,List) and (not val.marked)) :
                print("Freeing unreferenced List: "+str(val))
                itemsToRemove.add(val)
            elif(isinstance(val,Number) and (not val.marked)) :
                print("Freeing unreferenced Number: "+str(val))
                itemsToRemove.add(val)

        # Sweep
        for val in itemsToRemove :
            listCellCount = val.flattenedLength(None,None,None)
            self.cellInUseCount = self.cellInUseCount - listCellCount
            self.cellHeap.remove(val)

        print("Cells in use at end of GC: "+str(self.cellInUseCount))

