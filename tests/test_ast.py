from file_reader import FileReader
from pipeline import PipeLine
from tokenizer import Tokenizer
from parser import Parser
from my_ast import AST
from my_ast.end_node import EndNode
from my_ast.start_node import StartNode


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

def test_ast1():
    pipe = PipeLine(file_reader, tokenizer, parser, ast)
    val = pipe("tests/test1.s")
    for _ in val.res: pass

    res = []
    tmp = []
    curr = val.res.start
    while (type(curr) is not EndNode):
        if (type(curr) is StartNode and len(tmp) > 0):
            res.append(tmp)
            tmp = []
        tmp.append(f"{curr}({curr.left}, {curr.right})")
        if (type(curr.tail()) is EndNode) and curr.head():
            curr = curr.head()
        else:
            curr = curr.tail()
    res = [" -> ".join(v) for v in res]
    expect = ['StartNode(None, OpNode) -> OpNode(MOV, OprndNode) -> OprndNode(R1, OprndNode) -> OprndNode(200, StartNode)']
    assert res == expect

def test_ast2():
    pipe = PipeLine(file_reader, tokenizer, parser, ast)
    val = pipe("tests/test2.s")
    for _ in val.res: pass

    res = []
    tmp = []
    curr = val.res.start
    while (type(curr) is not EndNode):
        if (type(curr) is StartNode and len(tmp) > 0):
            res.append(tmp)
            tmp = []
        tmp.append(f"{curr}({curr.left}, {curr.right})")
        if (type(curr.tail()) is EndNode) and curr.head():
            curr = curr.head()
        else:
            curr = curr.tail()

    res = [" -> ".join(v) for v in res]
    expect = ['StartNode(None, OpNode) -> OpNode(CLRA, OprndNode) -> OprndNode(StartNode, EndNode)',
              'StartNode(None, OpNode) -> OpNode(MOV, OprndNode) -> OprndNode(R1, OprndNode) -> OprndNode(100, StartNode)',
              'StartNode(None, OpNode) -> OpNode(MOV, OprndNode) -> OprndNode(R2, OprndNode) -> OprndNode(200, StartNode)',
              'StartNode(None, OpNode) -> OpNode(ADD, OprndNode) -> OprndNode(R1, OprndNode) -> OprndNode(StartNode, EndNode)',
              'StartNode(None, OpNode) -> OpNode(ADD, OprndNode) -> OprndNode(R2, OprndNode) -> OprndNode(StartNode, EndNode)',
              'StartNode(None, OpNode) -> OpNode(MOVA, OprndNode) -> OprndNode(R1, OprndNode) -> OprndNode(StartNode, EndNode)']
    
    assert res == expect