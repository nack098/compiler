from collections.abc import Iterable
from collections import deque


class Parser:

    token: Iterable
    stack: deque[str] = []
    rules: dict[int, list[str]]
    parsing_table: dict[tuple[str, str], int]
    allow_any: list[str]
    empty_symbols: str
    starting_symbol: int
    current_symbol: str = ""

    def __init__(
            self,
            rules: dict[int, list[str]],
            parsing_table: dict[tuple[str, str], int],
            allow_any: Iterable = [],
            empty_symbols="e",
            starting_symbol:int = 0):
        self.rules = rules
        self.parsing_table = parsing_table
        self.starting_symbol = starting_symbol
        self.empty_symbols = empty_symbols
        self.allow_any = set(allow_any)
    
    def __iter__(self):
        return self
    
    def _parse(self, front):
        rule_idx = self.parsing_table.get((front, self.current_symbol))
        if not rule_idx:
            raise ValueError(f"Unknown rule for ({front}, {self.current_symbol})")
        self.stack.extend(reversed(self.rules[rule_idx]))

    def __next__(self):
        try:
            front = self.stack.pop()
            if (front == self.empty_symbols):
                return front
            if (self.current_symbol == ""):
                self.current_symbol = next(self.token)
            if (front in self.allow_any):
                self.stack.append(self.current_symbol)
                return front
            if (front == self.current_symbol):
                self.current_symbol = ""
                return front
            else:
                self._parse(front)
                return front
        except StopIteration:
            self._parse(front)
            return front
        except IndexError:
            raise StopIteration
    
    def __call__(self, token: Iterable):
        self.token = token
        self.stack.extend(self.rules[self.starting_symbol])
        return self