from interpreterextgc import *
from programextgc import *
import unittest

class GCTest(unittest.TestCase) :

    # Initialize some variables useful across tests
    def getSimpleList(self, gh) :
        l1 = [1,2,3,[4,5]]
        createdList = MiniLangUtils.pythonListToList(l1, gh)
        return createdList

    def test_simple_gc(self) :

        gh = Heap(10)
        atom = Number(0)
        createdList = self.getSimpleList(gh)
        print(createdList)
        self.assertTrue(len(gh.cellHeap) == 5)
        newList = BuiltIns.cons(atom,createdList,gh)
        emptyNt = dict()
        emptyFt = dict()
        print(createdList.eval(emptyNt,emptyFt))
        print(newList.eval(emptyNt,emptyFt))

        gh.collectGarbage(emptyNt,emptyFt)
        self.assertTrue(len(gh.cellHeap) == 0)

    def test_cdr_nomultipleAlloc(self) :
        l1 = getSimpleList()
        l2 = car(l1)
        self.assertTrue(True)



if __name__ == '__main__' :
    unittest.main()
