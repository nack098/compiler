from collections.abc import Iterable
from .estate import EState


class Tokenizer:

    raw: Iterable = []
    index: int = 0
    length: int = 0
    state: EState = EState.SKIP
    skip_symbols: list[str]

    def __init__(
            self,
            skip_symbols: list[str]):
        self.skip_symbols = skip_symbols
    
    def _state_machine(self):
        buf = ""
        while self.index < self.length:
            curr = self.raw[self.index]
            match self.state:
                case EState.SKIP:
                    if curr not in self.skip_symbols:
                        self.state = EState.TEXT
                        continue
                    self.index += 1
                case EState.TEXT:
                    if curr == ",":
                        self.state = EState.COLLON
                        return buf
                    if curr in self.skip_symbols:
                        self.state = EState.SKIP 
                        return buf
                    buf += curr
                    self.index += 1
                case EState.COLLON:
                    self.state = EState.TEXT
                    self.index += 1
                    return ","
        if buf:
            return buf
    
    def __iter__(self):
        return self
    
    def __next__(self):
        val = self._state_machine()
        if val:
            return val
        else:
            raise StopIteration
    
    def __call__(self, text:Iterable):
        self.state = EState.SKIP
        self.length = len(text)
        self.index = 0
        self.raw = text
        return self