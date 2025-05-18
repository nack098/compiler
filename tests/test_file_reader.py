from file_reader import FileReader

file_reader = FileReader()

def test_file1():
    res = "".join(file_reader("tests/test1.s"))
    with open("tests/test1.s") as test1:
        expect = test1.read()
        assert res == expect

def test_file2():
    res = "".join(file_reader("tests/test2.s"))
    with open("tests/test2.s") as test1:
        expect = test1.read()
        assert res == expect