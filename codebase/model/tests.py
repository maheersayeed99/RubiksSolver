import pytest
from cube import *

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

