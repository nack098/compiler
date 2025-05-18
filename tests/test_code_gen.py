from file_reader import FileReader
from pipeline import PipeLine
from tokenizer import Tokenizer
from parser import Parser
from my_ast import AST
from my_ast.end_node import EndNode
from my_ast.start_node import StartNode
from code_gen import CodeGen


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
ast = AST()
code_gen = CodeGen()

def test_ast1():
    pipe = PipeLine(file_reader, tokenizer, parser, ast, code_gen)
    val = pipe("tests/test1.s").unwrap()
    res = b""
    for v in val:
        res += v
    print(res.hex())
    assert res == b"\xb9\xc8\x00\x00\x00"

def test_ast2():
    pipe = PipeLine(file_reader, tokenizer, parser, ast, code_gen)
    val = pipe("tests/test2.s").unwrap()
    res = b""
    for v in val:
        res += v
    assert res == b"\x31\xc0\xb9\x64\x00\x00\x00\xba\xc8\x00\x00\x00\x01\xc1\x01\xc2\x89\xc1"