from collections.abc import Iterator
from my_ast import *

class CodeGen:

    tree: Iterator
    current_line: bytes
    last_instruction: bytes

    def __init__(self):
        pass

    def __iter__(self):
        return self

    def _state_machine(self, current_node):
        match current_node:
            case StartNode():
                if self.current_line:
                    val = self.current_line
                    return val
                else:
                    self.current_line = b""
            case OpNode():
                match str(current_node.head()):
                    case "CLRA":
                        self.current_line += b"\x31" + bytes([0b11000000])
                    case "MOV":
                        self.last_instruction = b"\xB8"
                    case "ADD":
                        self.last_instruction = b"\x01"
                    case "MOVA":
                        self.last_instruction = b"\x89"
            case OprndNode():
                if (current_node.tail() == EndNode):
                    return None
                match str(current_node.head()):
                    case "R1":
                        if self.last_instruction == b"\xB8":
                            self.current_line += b"\xB9"
                        elif self.last_instruction == "\x89":
                            self.current_line += b"\x89" + bytes([0b11001000])
                        else:
                            self.current_line += self.last_instruction
                            self.current_line += bytes([0b11000001])
                    case "R2":
                        if self.last_instruction == b"\xB8":
                            self.current_line += b"\xBA"
                        elif self.last_instruction == "\x89":
                            self.current_line += b"\x89" + bytes([0b11010000])
                        else:
                            self.current_line += self.last_instruction
                            self.current_line += bytes([0b11000010])
                    case "100":
                        self.current_line += int(str(current_node.head())).to_bytes(4, "little")
                    case "200":
                        self.current_line += int(str(current_node.head())).to_bytes(4, "little")
    
    def __next__(self):
        try:
            while (True):
                curr = next(self.tree)
                val = self._state_machine(curr)
                if val != None:
                    self.current_line = b""
                    return val

        except StopIteration:
            raise StopIteration

    def __call__(self, tree: Iterator):
        self.tree = tree
        self.current_line = b""
        self.last_instruction = b""
        return self