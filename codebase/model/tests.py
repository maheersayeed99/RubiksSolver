import pytest
from cube import *
import databases
def test_removeDuplicates():
    newCube = cube()
    assert(newCube.removeDuplicates(["a","b","c","d"]) == ["a","b","c","d"])
    assert(newCube.removeDuplicates(["a","b","b","d"]) == ["a","bb","d"])
    assert(newCube.removeDuplicates(["a","d"]) == ["a","d"])
    assert(newCube.removeDuplicates(["a"]) == ["a"])
    assert(newCube.removeDuplicates([]) == [])
    assert(newCube.removeDuplicates(["a","a","b","d"]) == ["aa","b","d"])
    assert(newCube.removeDuplicates(["a","a","a","d"]) == ["aa","a","d"])
    assert(newCube.removeDuplicates(["a","b","c","c"]) == ["a","b","cc"])
    assert(newCube.removeDuplicates(["a","a"]) == ["aa"])


def test_processString():
    newCube = cube()
    assert(newCube.processMoves(["l","l","l","l"]) == [])
    assert(newCube.processMoves(["l","l","l"]) == ["L"])
    assert(newCube.processMoves(["L","L","L"]) == ["l"])
    assert(newCube.processMoves(["L","l","L"]) == ["L"])
    assert(newCube.processMoves(["L","L"]) == ["LL"])
    assert(newCube.processMoves(["L","l"]) == [])
    assert(newCube.processMoves([]) == [])
    assert(newCube.processMoves(["L","L","L","d","D"]) == ["l"])
    assert(newCube.processMoves(["l","l","l", "R","d"]) == ["L","R","d"])


