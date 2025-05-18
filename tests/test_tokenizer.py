from file_reader import FileReader
from tokenizer import Tokenizer


file_reader = FileReader()
tokenizer = Tokenizer(skip_symbols={" ", "\n"})


def test_tokenizer_basic():
    expect = ["MOV", "R1", ",", "200"]
    tokenizer(file_reader("tests/test1.s"))
    tokens = list(tokenizer)
    assert tokens == expect


def test_tokenizer_multiline():
    text = """
        CLRA
        MOV R1,100
        MOV R2,200
        ADD R1
        ADD R2
        MOVA R1
    """
    expect = ["CLRA", "MOV", "R1", ",", "100", "MOV", "R2", ",", "200", "ADD", "R1", "ADD", "R2", "MOVA", "R1"]
    tokenizer(file_reader("tests/test2.s"))
    tokens = list(tokenizer)
    assert tokens == expect