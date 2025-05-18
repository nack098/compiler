from tokenizer import Tokenizer


tokenizer = Tokenizer(skip_symbols={" ", "\n"})


def test_tokenizer_basic():
    text = "MOV R1,200"
    expect = ["MOV", "R1", ",", "200"]
    tokenizer.set(text)
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
    tokenizer.set(text)
    tokens = list(tokenizer)
    assert tokens == expect