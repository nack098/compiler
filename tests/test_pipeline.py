from file_reader import FileReader
from pipeline import PipeLine
from tokenizer import Tokenizer
from parser import Parser


skip_symbols = {" ", "\n"}
rules = {
    0: ["asm"],
    1: ["op", "oprnd", "asm"],
    2: ["e"],
    3: ["CLRA"],
    4: ["MOV"],
    5: ["ADD"],
    6: ["MOVA"],
    7: ["reg", "param"],
    8: ["e"],
    9: [",", "num"],
    10: ["e"],
    11: ["R1"],
    12: ["R2"],
    13: ["100"],
    14: ["200"],
    15: ["e"]
}
parsing_table = {
    ("asm", "CLRA"): 1,
    ("asm", "MOV"): 1,
    ("asm", "ADD"): 1,
    ("asm", "MOVA"): 1,
    ("asm", ""): 2,
    ("op", "CLRA"): 3,
    ("op", "MOV"): 4,
    ("op", "ADD"): 5,
    ("op", "MOVA"): 6,
    ("oprnd", "R1"): 7,
    ("oprnd", "R2"): 7,
    ("oprnd", "CLRA"): 8,
    ("oprnd", "MOV"): 8,
    ("oprnd", "ADD"): 8,
    ("oprnd", "MOVA"): 8,
    ("oprnd", ""): 15,
    ("reg", "R1"): 11,
    ("reg", "R2"): 12,
    ("param", ","): 9,
    ("param", "CLRA"): 10,
    ("param", "MOV"): 10,
    ("param", "ADD"): 10,
    ("param", "MOVA"): 10,
    ("param", ""): 10,
    ("num", "100"): 13,
    ("num", "200"): 14,
}

file_reader = FileReader()
tokenizer = Tokenizer(skip_symbols=skip_symbols)
parser = Parser(rules=rules, parsing_table=parsing_table)


class Test1:
    def __call__(self, a):
        yield a

class Test2:
    def __call__(self, b):
        for i in b:
            yield i

class Test3:
    def __call__(self, c):
        for i in c:
            yield i + 10


def test_pipe():
    pipe = PipeLine(Test1())
    assert [10] == pipe(10).unwrap()

def test_parsing():
    pipe = PipeLine(Test1(), Test2())
    assert [10] == pipe(10).unwrap()

def test_manipulation():
    pipe = PipeLine(Test1(), Test2(), Test3())
    assert [20] == pipe(10).unwrap()

def test_integrate():
    pipe = PipeLine(file_reader, tokenizer, parser)
    res = pipe("tests/test2.s").unwrap()
    expect = [
        "asm","op", "CLRA", "oprnd", "e",
        "asm", "op", "MOV", "oprnd", "reg", "R1", "param", ",", "num", "100",
        "asm", "op", "MOV", "oprnd", "reg", "R2", "param", ",", "num", "200",
        "asm", "op", "ADD", "oprnd", "reg", "R1", "param", "e",
        "asm", "op", "ADD", "oprnd", "reg", "R2", "param", "e",
        "asm", "op", "MOVA", "oprnd", "reg", "R1", "param", "e", "asm", "e"]

    assert res == expect