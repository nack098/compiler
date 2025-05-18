from collections.abc import Iterable
from .estate import EState


class Tokenizer:

    raw: Iterable = []
    state: EState = EState.SKIP
    skip_symbols: list[str]

    def __init__(
            self,
            skip_symbols: list[str]):
        self.skip_symbols = skip_symbols
    
    def _state_machine(self):
        buf = ""
        try:
            if self.state != EState.COLLON:
                curr = next(self.raw)
            while True:
                match self.state:
                    case EState.SKIP:
                        if curr not in self.skip_symbols:
                            self.state = EState.TEXT
                            continue
                        curr = next(self.raw)
                    case EState.TEXT:
                        if curr == ",":
                            self.state = EState.COLLON
                            return buf
                        if curr in self.skip_symbols:
                            self.state = EState.SKIP 
                            if len(buf) > 0:
                                return buf
                            continue
                        buf += curr
                        curr = next(self.raw)
                    case EState.COLLON:
                        self.state = EState.TEXT
                        return ","
        except StopIteration:
            if buf:
                return buf
            raise StopIteration
    
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
        self.raw = text
        return self