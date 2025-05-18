from file_reader import FileReader
from tokenizer import Tokenizer
from parser import Parser
from my_ast import AST
from code_gen import CodeGen
from pipeline import PipeLine
from executable_gen import ExecutableGenerator

from sys import argv

from config import Config

def _main(path:str):
    proc = PipeLine(
                FileReader(),
                Tokenizer(skip_symbols=Config.skip_symbols),
                Parser(rules=Config.rules, parsing_table=Config.parsing_table),
                AST(),
                CodeGen(),
                ExecutableGenerator(os="linux"))
    print(f"Total binary size: {proc(path).unwrap()}")

def main():
    args = argv

    if len(args) == 1:
        raise ValueError("Unspecified path\nUsage: python -m compiler <PATH>")
    elif len(args) > 2:
        raise ValueError("Unknown command\nUsage python -m compiler <PATH>")

    path = args[1]
    _main(path)

if __name__ == "__main__":
    main()